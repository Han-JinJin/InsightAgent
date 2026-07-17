import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from graph_agent import run_graph_agent

app = FastAPI()

UPLOAD_DIR = "uploads"
CURRENT_FILE_PATH = "uploads/current.csv"


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Hello Daisy, FastAPI is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not file.filename.endswith(".csv"):
        return {
            "success": False,
            "message": "目前只支持上传CSV文件。"
        }

    with open(CURRENT_FILE_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "message": "CSV文件上传成功。",
        "filename": file.filename,
        "saved_as": CURRENT_FILE_PATH
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = run_graph_agent(request.question)
    return result

@app.get("/report")
def get_report():
    report_path = "reports/analysis_report.md"

    if not os.path.exists(report_path):
        return {
            "success": False,
            "message": "报告还没有生成，请先在 /chat 中输入：生成分析报告"
        }

    return FileResponse(
        report_path,
        media_type="text/markdown",
        filename="analysis_report.md"
    )


@app.get("/charts/{chart_name}")
def get_chart(chart_name: str):
    chart_path = os.path.join("reports", "charts", chart_name)

    if not os.path.exists(chart_path):
        return {
            "success": False,
            "message": "图表不存在，请先生成图表。"
        }

    return FileResponse(
        chart_path,
        media_type="image/png",
        filename=chart_name
    )