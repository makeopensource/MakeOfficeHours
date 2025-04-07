"""Configuration for MOH api server"""

import os


class Config:
    """Configuration class for MOJ api server, stores current configuration state of flask api"""

    def __init__(self):
        self.API_MODE = os.getenv("API_MODE", "Can not find mode")
