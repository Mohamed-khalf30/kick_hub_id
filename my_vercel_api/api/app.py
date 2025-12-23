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
async def predict(
    file: UploadFile = File(None),
    image_url: str = Form(None)
):
    """
    يقبل:
    - file (multipart)
    - أو image_url (form field)
    """
    if not file and not image_url:
        return JSONResponse(status_code=400, content={"error": "Provide file or image_url"})

    try:
        # 1️⃣ لو جاية كـ URL
        if image_url:
            result = client.predict(
                image=handle_file(image_url),
                api_name="/predict_id_gradio"
            )
            return {"result": result}

        # 2️⃣ لو جاية كـ File
        if file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            result = client.predict(
                image=tmp_path,
                api_name="/predict_id_gradio"
            )

            # حذف الملف المؤقت بعد الاستخدام
            try:
                os.remove(tmp_path)
            except Exception:
                pass

            return {"result": result}

    except Exception as e:
        # لو حصل أي خطأ يرجع JSON بدل crash
        return JSONResponse(status_code=500, content={"error": str(e)})
