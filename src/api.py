import uvicorn
from fastapi import FastAPI
from request_types.analyze import analyze

class VisipanyaAPI(FastAPI):
    def __init__(self) -> None:
        super().__init__()
        self.add_api_route("/analyze", analyze, methods=["POST"])


def start_api(host, port):
    uvicorn.run(
        app=VisipanyaAPI(),
        host=host,
        port=port
    )