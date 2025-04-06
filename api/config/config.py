import os


class Config:
    def __init__(self):
        self.APP_MODE = os.getenv("APP_MODE", default="prod")
        pass
