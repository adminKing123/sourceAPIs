import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from flask import Response, stream_with_context

load_dotenv()


def download_file_stream(github_path):
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{CONFIG.GITHUB1.GITHUB_USERNAME}/"
        f"{CONFIG.GITHUB1.GITHUB_REPO_NAME}/"
        f"{CONFIG.GITHUB1.GITHUB_BRANCH_NAME}/"
        f"{github_path}"
    )

    filename = os.path.basename(github_path)

    r = requests.get(raw_url, stream=True)
    r.raise_for_status()

    return Response(
        stream_with_context(r.iter_content(chunk_size=8192)),
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": r.headers.get("Content-Type", "application/octet-stream")
        }
    )



class GithubConfig:
    def __init__(self, GITHUB_TOKEN, GITHUB_BRANCH_NAME, GITHUB_REPO_NAME, GITHUB_USERNAME):
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.GITHUB_BRANCH_NAME = GITHUB_BRANCH_NAME
        self.GITHUB_REPO_NAME = GITHUB_REPO_NAME
        self.GITHUB_USERNAME = GITHUB_USERNAME

class CONFIG:
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    GITHUB1 = GithubConfig(
        GITHUB_TOKEN=os.getenv("GITHUB1_TOKEN"),
        GITHUB_BRANCH_NAME=os.getenv("GITHUB1_BRANCH_NAME"),
        GITHUB_REPO_NAME=os.getenv("GITHUB1_REPO_NAME"),
        GITHUB_USERNAME=os.getenv("GITHUB1_USERNAME"),
    )

app = Flask(__name__)
CORS(app)

@app.route("/download/<path:github_path>")
def download(github_path):
    return download_file_stream(github_path)

app.run(host='0.0.0.0', port=CONFIG.PORT, debug=CONFIG.DEBUG)