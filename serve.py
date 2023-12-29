import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse

from core import VectorFormat, any2any

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
