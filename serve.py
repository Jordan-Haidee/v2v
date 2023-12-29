from pathlib import Path
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from core import any2any, VectorFormat
import tempfile

app = FastAPI()
temp_directory = Path(tempfile.gettempdir())


@app.post("/vector2vector")
def convert(vector_file: UploadFile = Form(...), target_type: VectorFormat = Form(...)):
    task_id = str(uuid.uuid4())
    task_dir = temp_directory / task_id
    task_dir.mkdir()
    src = (task_dir / task_id).with_suffix(Path(vector_file.filename).suffix)
    dst = src.with_suffix(target_type)
    with open(src, "wb") as f:
        f.write(vector_file.file.read())
    any2any(src, dst)
    return FileResponse(dst)
