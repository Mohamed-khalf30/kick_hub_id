from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from gradio_client import Client, handle_file
import requests

app = FastAPI()

# اسم الـ Space على Hugging Face
GRADIO_SPACE = "MohamedKhalf30/ID_verfication_3"
API_NAME = "/predict_id_gradio"

client = Client(GRADIO_SPACE)

@app.post("/predict")
async def predict(image_url: str = Form(...)):
    """
    توقع الرقم القومي من رابط صورة
    """
    try:
        # تحميل الصورة من الرابط
        resp = requests.get(image_url)
        if resp.status_code != 200:
            return JSONResponse(content={"status": "failed", "message": "فشل تحميل الصورة"}, status_code=400)

        # حفظ الصورة مؤقتًا
        with open("/tmp/temp_image.jpg", "wb") as f:
            f.write(resp.content)

        # استخدام Gradio Client
        result = client.predict(
            image=handle_file("/tmp/temp_image.jpg"),
            api_name=API_NAME
        )

        return JSONResponse(content={"status": "success", "result": result})

    except Exception as e:
        return JSONResponse(content={"status": "failed", "message": str(e)}, status_code=500)
