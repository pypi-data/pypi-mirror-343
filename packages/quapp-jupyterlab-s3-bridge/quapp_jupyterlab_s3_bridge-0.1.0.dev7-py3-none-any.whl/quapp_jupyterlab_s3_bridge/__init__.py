# try:
#     from ._version import __version__
# except ImportError:
#     import warnings
#     warnings.warn("Importing 'quapp_jupyterlab_s3_bridge' outside a proper installation.")
#     __version__ = "dev"


# def _jupyter_labextension_paths():
#     """
#     Khai báo labextension (front-end) để JupyterLab nhận biết.
#     """
#     return [{
#         "src": "labextension",
#         "dest": "quapp-jupyterlab-s3-bridge"
#     }]


# def _jupyter_server_extension_paths():
#     """
#     Cho phép Jupyter <3 tự động load server extension.
#     Với Jupyter Server 2.x / JupyterLab 4.x, entry point này có thể không cần thiết,
#     nhưng không gây hại khi có.
#     """
#     return [{
#         "module": "quapp_jupyterlab_s3_bridge"
#     }]


# def load_jupyter_server_extension(nbapp):
#     """
#     Load server extension:
#       - Đăng ký các route (handler) cho S3.
#       - Bạn có thể bổ sung gọi initialize_root() ở đây nếu muốn.
#     """
#     from .handler import setup_handlers
#     web_app = nbapp.web_app
#     setup_handlers(web_app)
#     nbapp.log.info("Registered /upload-s3 route for S3 uploading.")


# quapp_jupyterlab_s3_bridge/__init__.py
try:
    from ._version import __version__
except ImportError:
    __version__ = "dev"

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "quapp_jupyterlab_s3_bridge"
    }]

def _jupyter_server_extension_points():
    from .app import S3BridgeExtensionApp
    return [{
        "module": __name__,
        "app": S3BridgeExtensionApp
    }]