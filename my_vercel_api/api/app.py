from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from gradio_client import Client, handle_file
import requests
import shutil
import os

app = FastAPI(title="Egyptian ID Extractor")

# =====================
# 🔹 إعداد Gradio Client
# =====================
GRADIO_SPACE = "MohamedKhalf30/ID_verfication_3"
API_NAME = "/predict_id_gradio"
client = Client(GRADIO_SPACE)

# =====================
# 🔹 Endpoint الأساسي
# =====================
@app.post("/predict")
async def predict(
    image_url: str = Form(None),
    file: UploadFile = File(None)
):
    """
    توقع الرقم القومي من:
    1️⃣ رابط صورة (image_url)
    2️⃣ رفع صورة مباشرة (file)
    """
    try:
        tmp_path = "/tmp/temp_image.jpg"

        if image_url:
            # تحميل الصورة من الإنترنت
            resp = requests.get(image_url, stream=True)
            if resp.status_code != 200:
                return JSONResponse(content={"status": "failed", "message": "فشل تحميل الصورة"}, status_code=400)
            with open(tmp_path, "wb") as f:
                shutil.copyfileobj(resp.raw, f)

        elif file:
            # رفع الصورة مباشرة
            with open(tmp_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

        else:
            return JSONResponse(content={"status": "failed", "message": "يرجى إرسال image_url أو رفع ملف"}, status_code=400)

        # استخدام Gradio Client للتنبؤ
        result = client.predict(
            image=handle_file(tmp_path),
            api_name=API_NAME
        )

        # حذف الصورة المؤقتة
        os.remove(tmp_path)

        return JSONResponse(content={"status": "success", "result": result})

    except Exception as e:
        return JSONResponse(content={"status": "failed", "message": str(e)}, status_code=500)

# =====================
# 🔹 Health Check
# =====================
@app.get("/health")
async def health():
    return {"status": "healthy", "message": "✅ API جاهز"}
