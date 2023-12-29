from pathlib import Path
import uuid
import gradio as gr
from core import VectorFormat
import httpx
import tempfile


def gradio_pipeline(input_files: list, target_type: str):
    output_files = []
    task_id = str(uuid.uuid4())
    task_dir = Path(tempfile.gettempdir()) / task_id
    task_dir.mkdir()
    url = "http://127.0.0.1:8005/vector2vector/"
    for file in input_files:
        with open(file.name, "rb") as f:
            response = httpx.post(
                url,
                data={"target_type": target_type},
                files={"vector_file": f},
                follow_redirects=True,
            )
        origin_name = Path(file.name).stem
        save_path = task_dir / ("{}_converted{}".format(origin_name, target_type))
        with open(save_path, "wb") as f:
            f.write(response.content)
        output_files.append(str(save_path))
    return output_files


with gr.Blocks(theme=gr.themes.Soft(), title="vector2vector") as demo:
    with gr.Row():
        input_files_area = gr.Files(label="Input Files")
        output_files_area = gr.Files(label="Output Files")
    with gr.Row():
        with gr.Column():
            target_type_dropdown = gr.Dropdown(
                choices=map(lambda x: x.value, VectorFormat),
                label="Target Vector Type",
                show_label=False,
            )
            submit_btn = gr.Button(value="Submit")
    submit_btn.click(
        fn=gradio_pipeline,
        inputs=[input_files_area, target_type_dropdown],
        outputs=output_files_area,
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8006)
