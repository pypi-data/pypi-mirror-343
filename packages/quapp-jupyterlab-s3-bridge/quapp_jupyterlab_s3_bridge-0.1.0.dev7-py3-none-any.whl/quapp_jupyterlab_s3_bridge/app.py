# app.py
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin
from .manager import S3SelectiveContentsManager
import os
import re
import tornado.web

class S3BridgeExtensionApp(ExtensionApp, ExtensionAppJinjaMixin):
    """
    ExtensionApp cho S3 Bridge
    """
    name = "quapp_jupyterlab_s3_bridge"
    default_url = "/s3bridge"
    load_other_extensions = True

    static_paths = []
    template_paths = []

    @property
    def handlers(self):
        from .handler import VersionsHandler, PresignedUrlsHandler, UploadS3Handler
        base_url = self.settings.get("base_url", "/").rstrip("/")  # Lấy base_url và loại bỏ trailing '/'
        base_url_regex = re.escape(base_url)  # Escape chuỗi base_url để đảm bảo các ký tự đặc biệt được xử lý

        return [
            (rf"{base_url_regex}/s3bridge/upload-s3", UploadS3Handler),
            (rf"{base_url_regex}/s3bridge/versions", VersionsHandler),
            (rf"{base_url_regex}/s3bridge/versions/([^/]+)", PresignedUrlsHandler),
        ]

    def initialize_settings(self):
        cm = self.serverapp.contents_manager
        if not isinstance(cm, S3SelectiveContentsManager):
            self.log.info("Replacing serverapp.contents_manager with S3SelectiveContentsManager")
            cm = S3SelectiveContentsManager(
                root_dir=os.environ.get("ROOT_DIR", "/home/jovyan"),
                backend_url=os.environ.get("BACKEND_URL", "http://192.168.10.63:8090"),
                function_id=os.environ.get("FUNCTION_ID", "674")
            )
            self.serverapp.contents_manager = cm
        self.serverapp.web_app.settings.update({"contents_manager": cm})
        self.log.info("Settings updated: %s", self.serverapp.web_app.settings)

    async def _start_jupyter_server_extension(self):
        self.log.info("Starting S3BridgeExtensionApp")
        if hasattr(self.serverapp.contents_manager, "initialize_root"):
            self.log.info("Calling initialize_root() on S3SelectiveContentsManager")
            await self.serverapp.contents_manager.initialize_root()
        await super()._start_jupyter_server_extension()

    async def stop_extension(self):
        self.log.info("Stopping S3BridgeExtensionApp")
        # Cleanup nếu cần

if __name__ == "__main__":
    S3BridgeExtensionApp.launch_instance()
