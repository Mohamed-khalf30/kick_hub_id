from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from gradio_client import Client, handle_file
import tempfile
import os

app = FastAPI(
    title="ID Verification API",
    description="FastAPI wrapper over Gradio Space",
    version="1.0"
)

# اسم الـ Gradio Space
client = Client("MohamedKhalf30/ID_verfication_3")


@app.get("/health")
def health():
    """Endpoint للتأكد من إن الـ Function شغالة"""
    return {"status": "ok"}


@app.post("/predict")
async def predict(image_url: str = Form(...)):
    try:
        result = client.predict(
            image=handle_file(image_url),
            api_name="/predict_id_gradio"
        )
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

