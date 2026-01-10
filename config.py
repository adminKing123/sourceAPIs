import os
from dotenv import load_dotenv

load_dotenv()

class GithubConfig:
    def __init__(self, GITHUB_TOKEN, GITHUB_BRANCH_NAME, GITHUB_REPO_NAME, GITHUB_USERNAME):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.GITHUB_BRANCH_NAME = GITHUB_BRANCH_NAME
        self.GITHUB_REPO_NAME = GITHUB_REPO_NAME
        self.GITHUB_USERNAME = GITHUB_USERNAME

class UploadsConfig:
    def __init__(self, UPLOAD_FOLDER):
        self.UPLOAD_FOLDER = UPLOAD_FOLDER

class CONFIG:
    HOST = os.getenv("HOST", "https://sourceapis.onrender.com")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    GITHUB1 = GithubConfig(
        GITHUB_TOKEN=os.getenv("GITHUB1_TOKEN"),
        GITHUB_BRANCH_NAME=os.getenv("GITHUB1_BRANCH_NAME"),
        GITHUB_REPO_NAME=os.getenv("GITHUB1_REPO_NAME"),
        GITHUB_USERNAME=os.getenv("GITHUB1_USERNAME"),
    )
    UPLOAD1 = UploadsConfig(
        UPLOAD_FOLDER=os.getenv("UPLOAD1_FOLDER", "sources")
    )