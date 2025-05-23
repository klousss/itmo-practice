from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from PIL import Image
import io
from surya.ocr import run_ocr
from surya.model.detection import segformer
from surya.model.recognition.model import load_model
from surya.model.recognition.processor import load_processor

app = FastAPI()

# загрузите модели один раз
det_processor = segformer.load_processor()
det_model = segformer.load_model()
rec_model = load_model()
rec_processor = load_processor()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head><meta charset="UTF-8"><title>OCR на Surya</title></head>
    <body style="font-family:sans-serif;max-width:600px;margin:2em auto">
      <h1>OCR-сервис на Surya</h1>
      <input type="file" id="fileInput" accept="image/*"/>
      <button onclick="doOCR()" style="margin-left:1em">Распознать</button>
      <pre id="output" style="white-space:pre-wrap;margin-top:1em;"></pre>
      <script>
        async function doOCR() {
          const out = document.getElementById('output');
          out.textContent = 'Загрузка…';
          const file = document.getElementById('fileInput').files[0];
          if (!file) { out.textContent = 'Выберите файл'; return; }
          const form = new FormData();
          form.append('file', file);
          try {
            const res = await fetch('/ocr', { method:'POST', body:form });
            const json = await res.json();
            out.textContent = json.text ?? json.error;
          } catch (e) {
            out.textContent = 'Ошибка: ' + e;
          }
        }
      </script>
    </body>
    </html>
    """

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    langs = ["en"]
    preds = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)
    text = " ".join([ln.text for ln in preds[0].text_lines])
    return {"text": text}
