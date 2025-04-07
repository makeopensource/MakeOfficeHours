"""Configuration for MOH api server"""

import os


class Config:
    """Configuration class for MOJ api server, stores current configuration state of flask api
    """
    def __init__(self):
        self.app_mode = os.getenv("APP_MODE", default="prod")
