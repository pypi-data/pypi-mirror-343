# handler.py
import json
import re
import tornado.web
from jupyter_server.base.handlers import APIHandler
from .manager import S3SelectiveContentsManager

def get_cognito_id_token(handler) -> str:
    """
    Quét qua tất cả các cookie và tìm cookie có tên phù hợp với pattern:
      CognitoIdentityServiceProvider.<something>.<something>.idToken
    Nếu tìm thấy, trả về giá trị của cookie; nếu không, trả về None.
    """
    pattern = re.compile(r'^CognitoIdentityServiceProvider\..+\.idToken$')
    for name in handler.request.cookies:
        if pattern.match(name):
            return handler.get_cookie(name)
    return None

class VersionsHandler(APIHandler):
    @tornado.web.authenticated
    async def get(self):
        cm = self.settings.get("contents_manager")
        if not isinstance(cm, S3SelectiveContentsManager):
            self.set_status(400)
            self.finish(json.dumps({"error": "Not S3SelectiveContentsManager"}))
            return
        try:
            versions = cm.get_versions_list()
            self.finish(json.dumps({"data": versions}))
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))

class PresignedUrlsHandler(APIHandler):
    @tornado.web.authenticated
    async def patch(self, version: int):
        # Kiểm tra version phải là số
        if not str(version).isdigit():
            self.set_status(400)
            self.finish(json.dumps({"error": "Invalid version"}))
            return
        version = int(version)
        cm = self.settings.get("contents_manager")
        if not isinstance(cm, S3SelectiveContentsManager):
            self.set_status(400)
            self.finish(json.dumps({"error": "Not S3SelectiveContentsManager"}))
            return
        try:
            urls = cm.update_file_list(version)
            self.finish(json.dumps({"data": urls}))
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))

class UploadS3Handler(APIHandler):
    @tornado.web.authenticated
    async def post(self):
        # Dùng helper get_cognito_id_token để lấy JWT idToken theo pattern của Cognito.
        jwt_id_token = get_cognito_id_token(self)
        if jwt_id_token is None:
            self.set_status(401)
            self.finish(json.dumps({"error": "JWT idToken not found in cookie"}))
            return

        cm = self.settings.get("contents_manager")
        if not isinstance(cm, S3SelectiveContentsManager):
            self.set_status(400)
            self.finish(json.dumps({"error": "Not S3SelectiveContentsManager"}))
            return
        try:
            # Truyền JWT vào hàm upload_to_backend để gọi API backend.
            await cm.upload_to_backend(description="FileBrowser Save S3", jwt=jwt_id_token)
            self.finish(json.dumps({"status": "ok"}))
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))
