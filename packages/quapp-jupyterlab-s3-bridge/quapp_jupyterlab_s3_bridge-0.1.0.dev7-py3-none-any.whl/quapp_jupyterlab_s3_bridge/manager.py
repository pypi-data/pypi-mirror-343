# manager.py
import os
import logging
import shutil
import re
import requests
import aiofiles
import time

from typing import Any, Dict, Optional, List
from datetime import datetime, timezone
from jupyter_server.services.contents.manager import AsyncContentsManager
from jupyter_server.services.contents.checkpoints import Checkpoints
from jupyter_server.utils import ensure_async
from tornado.web import HTTPError
from tornado.ioloop import IOLoop

logger = logging.getLogger(__name__)

SPECIAL_REQUIREMENTS = {"requirements.txt", "handler.py"}
ALLOWED_EXTENSIONS = {".py", ".txt", ".ipynb"}

project_id = int(os.environ.get("PROJECT_ID", 349))

class NoOpCheckpoints(Checkpoints):
    """
    Checkpoints “trống” để tránh NotImplementedError.
    Không dùng checkpoint thật.
    """
    async def create_checkpoint(self, contents_mgr, path):
        return {}

    async def list_checkpoints(self, path):
        return []

    async def restore_checkpoint(self, contents_mgr, checkpoint, path):
        pass

    async def delete_checkpoint(self, checkpoint_id, path):
        pass

    async def delete_all_checkpoints(self, path):
        pass

    async def rename_all_checkpoints(self, old_path, new_path):
        pass


class S3SelectiveContentsManager(AsyncContentsManager):
    """
    Mô hình 2 luồng:
      1) Khi start JupyterLab => __init__ => add_callback => initialize_root()
         -> Gọi backend API “pull object” về local
      2) Khi user muốn “upload” => gọi upload_to_backend() => POST /api/v1/functions/{functionId}/versions
         -> Gửi các file local lên backend server.

    Tất cả thao tác (save, rename, delete) ở local => “offline”.
    """

    def __init__(self, root_dir=None, backend_url=None, function_id=None, **kwargs):
        super().__init__(**kwargs)
        # root_dir local
        self.root_dir = root_dir or os.environ.get("ROOT_DIR", "/home/jovyan")
        # mock server URL
        self.backend_url = backend_url or os.environ.get("BACKEND_URL", "http://192.168.10.63:8090")
        # function ID
        self.function_id = function_id or os.environ.get("FUNCTION_ID", "674")
        
        # JWT hệ thống dùng cho các API gọi khi không có thông tin từ request (ví dụ lúc khởi tạo)
        self.system_jwt = os.environ.get("SYSTEM_JWT", "")

        os.makedirs(self.root_dir, exist_ok=True)
        logger.info("Init => root_dir=%s, backend_url=%s, function_id=%s",
                    self.root_dir, self.backend_url, self.function_id)

        # Ngay khi khởi tạo, đăng ký gọi initialize_root() với JWT hệ thống trong IOLoop
        IOLoop.current().add_callback(self._init_root_wrapper)

    async def _init_root_wrapper(self):
        """
        Hàm async gọi initialize_root(), bắt ngoại lệ.
        Sử dụng self.system_jwt cho việc fetch đối tượng từ backend khi không có JWT từ request.
        """
        try:
            await self.initialize_root(jwt=self.system_jwt)
        except Exception as e:
            logger.exception("Error in initialize_root at startup: %s", e)

    def _build_headers(self, jwt: str) -> Dict[str, str]:
        """
        Xây dựng headers yêu cầu backend, bao gồm cả JWT.
        """
        return {
            "x-project-id": str(project_id),
            "Authorization": f"Bearer {jwt}"
        }

    async def initialize_root(self, jwt: str = None):
        """
        Pull object từ backend:
          1) GET /api/v1/functions/{functionId}/versions
          2) Lấy phiên bản mới nhất
          3) GET /api/v1/functions/{functionId}/versions/{versionId} => lấy presigned URLs
          4) Download về local.

        Yêu cầu có jwt để gọi backend.
        """
        jwt = jwt or self.system_jwt
        if not jwt:
            logger.error("No JWT available for initialize_root")
            return

        logger.info("Pull object from backend... functionId=%s", self.function_id)
        try:
            versions_url = f"{self.backend_url}/api/v1/functions/{self.function_id}/versions"
            headers = self._build_headers(jwt)
            resp = requests.get(versions_url, headers=headers)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                logger.warning("No versions found => skip pull.")
                return

            # Lấy version mới nhất
            latest_version = data[0]
            logger.info("Latest version => id=%s", latest_version["id"])
            self.version_id = latest_version["id"]

            presign_url = f"{versions_url}/{self.version_id}"
            resp2 = requests.get(presign_url, headers=headers)
            resp2.raise_for_status()
            presigned_list = resp2.json().get("data", [])
            if not presigned_list:
                logger.warning("No presigned URLs found => skip pull.")
                return
            logger.info("Presigned URLs => %d items", len(presigned_list))
            for url_ in presigned_list:
                fname = self._extract_filename_from_url(url_)
                logger.info("Downloading => %s => %s", url_, fname)
                r_file = requests.get(url_)
                if r_file.ok:
                    local_path = os.path.join(self.root_dir, fname)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(r_file.content)
                else:
                    logger.warning("Download fail => %s => status=%d", url_, r_file.status_code)
        except Exception as e:
            logger.exception("Error pulling object: %s", e)

    @property
    def checkpoints(self):
        return NoOpCheckpoints()

    # ------------------------------------------------------
    # Overriding Jupyter methods
    # ------------------------------------------------------
    async def get(self, path: str, content: bool = True, type=None, format=None, **kwargs) -> Dict[str, Any]:
        abs_path = self._abs_path(path)
        if not os.path.exists(abs_path):
            raise HTTPError(404, f"Path not found: {path}")
        if os.path.isdir(abs_path):
            return await ensure_async(self._dir_model(path, abs_path, content))
        else:
            return await ensure_async(self._file_model(path, abs_path, content, format))

    async def save(self, model: Dict[str, Any], path: str) -> Dict[str, Any]:
        abs_path = self._abs_path(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        file_type = model.get("type", "file")
        content_val = model.get("content")
        base_name = os.path.basename(path)
        if file_type == "directory":
            if not re.match(r'^[A-Za-z0-9_-]+$', base_name):
                raise HTTPError(403, f"Invalid folder name => {base_name}")
            os.makedirs(abs_path, exist_ok=True)
            dir_model = await ensure_async(self._dir_model(path, abs_path, content=False))
            dir_model["content"] = None
            dir_model["format"] = None
            return dir_model

        ext = self._get_ext(base_name)
        if ext and ext not in ALLOWED_EXTENSIONS:
            raise HTTPError(403, f"Extension not allowed => {ext}")

        if file_type == "notebook":
            import json
            text = json.dumps(content_val)
            write_bytes = text.encode("utf-8")
        else:
            fmt = model.get("format")
            if fmt == "base64":
                import base64
                write_bytes = base64.b64decode(content_val)
            else:
                if isinstance(content_val, str):
                    write_bytes = content_val.encode("utf-8")
                elif isinstance(content_val, bytes):
                    write_bytes = content_val
                else:
                    raise HTTPError(400, "Unknown file content format")
        async with aiofiles.open(abs_path, "wb") as f:
            await f.write(write_bytes)

        file_model = await ensure_async(self._file_model(path, abs_path, content=True, format=None))
        if not write_bytes:
            file_model["content"] = None
            file_model["format"] = None
        return file_model

    async def new_untitled(self, path: str, type: str = '', ext: str = '') -> Dict[str, Any]:
        name = self._new_name(type, ext)
        new_path = os.path.join(path, name)
        now_time = datetime.now(timezone.utc).isoformat()
        if type == "notebook":
            abs_path = self._abs_path(new_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            nb_json = {
                "cells": [],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5
            }
            import json
            with open(abs_path, "w", encoding="utf-8") as f:
                json.dump(nb_json, f)
            return {
                "name": name,
                "path": new_path,
                "type": "notebook",
                "mimetype": None,
                "writable": True,
                "created": now_time,
                "last_modified": now_time,
                "content": None,
                "format": None
            }
        elif type == "directory":
            model = {"type": "directory", "content": None, "format": None}
        else:
            model = {"type": "file", "content": "", "format": "text"}
        return await self.save(model, new_path)

    async def delete_file(self, path: str) -> None:
        abs_path = self._abs_path(path)
        if not os.path.exists(abs_path):
            raise HTTPError(404, f"{path} not found")
        base_name = os.path.basename(path)
        if base_name in SPECIAL_REQUIREMENTS:
            raise HTTPError(403, f"Cannot delete '{base_name}'")
        if os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
        else:
            os.remove(abs_path)
        logger.info("Deleted local => %s", abs_path)

    async def rename_file(self, old_path: str, new_path: str) -> None:
        old_abs = self._abs_path(old_path)
        new_abs = self._abs_path(new_path)
        if not os.path.exists(old_abs):
            raise HTTPError(404, f"{old_path} not found")
        old_name = os.path.basename(old_path)
        if old_name in SPECIAL_REQUIREMENTS:
            raise HTTPError(403, f"Cannot rename or move '{old_name}'")
        if os.path.isdir(old_abs):
            new_name = os.path.basename(new_path)
            if not re.match(r'^[A-Za-z0-9_-]+$', new_name):
                raise HTTPError(403, f"Invalid folder rename => {new_name}")
        os.makedirs(os.path.dirname(new_abs), exist_ok=True)
        try:
            shutil.move(old_abs, new_abs)
        except Exception as e:
            logger.exception("rename error: %s", e)
            raise HTTPError(500, f"Rename failed: {e}")
        logger.info("Renamed => %s -> %s", old_path, new_path)

    # ------------------------------------------------------
    # Custom: upload_to_backend
    # ------------------------------------------------------
    async def upload_to_backend(self, description: str = "", jwt: str = None):
        """
        Quét file local và gửi POST request chứa templateFiles và description.
        Yêu cầu có jwt để gọi backend.
        """
        jwt = jwt or self.system_jwt
        if not jwt:
            logger.error("No JWT provided for upload_to_backend")
            return

        logger.info("upload_to_backend => scanning local dir: %s", self.root_dir)
        all_files = []
        for root, dirs, files in os.walk(self.root_dir):
            for fname in files:
                rel_dir = os.path.relpath(root, self.root_dir)
                rel_path = fname if rel_dir == "." else os.path.join(rel_dir, fname)
                ext = self._get_ext(fname)
                if ext and ext not in ALLOWED_EXTENSIONS:
                    logger.info("Skipping file => %s", rel_path)
                    continue
                all_files.append(rel_path)

        template_files = []
        for fpath in all_files:
            abs_f = self._abs_path(fpath)
            ext = self._get_ext(fpath)
            lang = "python" if ext == ".py" else "text"
            with open(abs_f, "rb") as f:
                data = f.read()
            data_list = list(data)
            template_files.append({
                "filename": fpath,
                "language": lang,
                "content": data_list
            })

        body = {
            "templateFiles": template_files,
            "description": description
        }

        url_update = f"{self.backend_url}/api/v1/functions/{self.function_id}/versions"
        headers = self._build_headers(jwt)
        logger.info("POST => %s", url_update)
        logger.info("templateFiles => %d items", len(template_files))
        try:
            resp = requests.post(url_update, json=body, headers=headers)
            resp.raise_for_status()
            logger.info("Upload success => version created => %s", resp.text)
        except Exception as e:
            logger.exception("Upload to backend error: %s", e)

    def get_versions_list(self, jwt: str = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách version từ backend.
        Yêu cầu có jwt để gọi backend.
        """
        jwt = jwt or self.system_jwt
        try:
            versions_url = f"{self.backend_url}/api/v1/functions/{self.function_id}/versions"
            headers = self._build_headers(jwt)
            resp = requests.get(versions_url, headers=headers)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            return data
        except Exception as e:
            logger.exception("Error getting versions list: %s", e)
            return []
    
    def update_file_list(self, version: int, jwt: str = None):
        """
        Cập nhật danh sách file theo version mới.
        Yêu cầu có jwt để gọi backend.
        """
        jwt = jwt or self.system_jwt
        try:
            versions_url = f"{self.backend_url}/api/v1/functions/{self.function_id}/versions"
            headers = self._build_headers(jwt)
            resp = requests.get(versions_url, headers=headers)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                logger.warning("No versions found => skip pull.")
                return []
            logger.info("Versions => %d items", len(data))
            for versionItem in data:
                if versionItem["version"] == version:
                    new_version = versionItem["id"]
                    break
            else:
                raise HTTPError(404, f"version not found: v{version}")
            current_version_files = []
            new_version_files = []
            for versionItem in data:
                if versionItem["id"] == self.version_id:
                    for fileItem in versionItem["files"]:
                        file_name = fileItem["key"].split("/")[-1]
                        current_version_files.append(file_name)
                if versionItem["id"] == new_version:
                    for fileItem in versionItem["files"]:
                        file_name = fileItem["key"].split("/")[-1]
                        new_version_files.append(file_name)
            for fileItem in current_version_files:
                if fileItem not in new_version_files:
                    logger.info("Deleting file => %s", fileItem)
                    abs_path = os.path.join(self.root_dir, fileItem)
                    if os.path.exists(abs_path):
                        os.remove(abs_path)
                    else:
                        logger.warning("File not found => %s", abs_path)
            if current_version_files or new_version_files:
                current_version_files.clear()
                new_version_files.clear()
            presign_url = f"{versions_url}/{new_version}"
            resp2 = requests.get(presign_url, headers=headers)
            resp2.raise_for_status()
            presigned_list = resp2.json().get("data", [])
            if not presigned_list:
                logger.warning("No presigned URLs found => skip pull.")
                return []
            logger.info("Presigned URLs => %d items", len(presigned_list))
            for url_ in presigned_list:
                fname = self._extract_filename_from_url(url_)
                logger.info("Downloading => %s => %s", url_, fname)
                r_file = requests.get(url_)
                if r_file.ok:
                    local_path = os.path.join(self.root_dir, fname)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(r_file.content)
                else:
                    logger.warning("Download fail => %s => status=%d", url_, r_file.status_code)
        except Exception as e:
            logger.exception("Error pulling object: %s", e)

    # ------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------
    def _abs_path(self, path: str) -> str:
        return os.path.join(self.root_dir, path.strip("/\\"))

    def _get_ext(self, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return ext.lower()

    def _new_name(self, type_: str, ext: str) -> str:
        ts = int(time.time())
        if type_ == "notebook":
            return f"Untitled-{ts}.ipynb"
        elif type_ == "directory":
            return f"UntitledFolder-{ts}"
        elif ext:
            return f"untitled-{ts}{ext}"
        else:
            return f"untitled-{ts}"

    def _file_model(self, path: str, abs_path: str, content: bool, format: Optional[str] = None):
        from jupyter_server.services.contents.filemanager import FileContentsManager
        fm = FileContentsManager()
        fm.root_dir = self.root_dir
        model = fm.get(path, content=content, type=None, format=format)
        model["hash"] = ""
        model["hash_algorithm"] = "md5"
        return model

    def _dir_model(self, path: str, abs_path: str, content: bool):
        from jupyter_server.services.contents.filemanager import FileContentsManager
        fm = FileContentsManager()
        fm.root_dir = self.root_dir
        model = fm.get(path, content=content, type='directory', format=None)
        model["hash"] = ""
        model["hash_algorithm"] = "md5"
        if not content:
            model["content"] = None
            model["format"] = None
        return model

    def _extract_filename_from_url(self, url_: str) -> str:
        import urllib.parse
        parsed = urllib.parse.urlparse(url_)
        segments = parsed.path.split("/")
        fname = segments[-1] if segments else "unknown.bin"
        return fname

    async def is_hidden(self, path: str) -> bool:
        return False
    
    async def file_exists(self, path: str) -> bool:
        return False
