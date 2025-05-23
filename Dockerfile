FROM python:3.9.6

# системная библиотека для OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# создаём рабочую папку
WORKDIR /code

# копируем и ставим зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# копируем весь FastAPI-код (там у вас main.py и статический HTML в home())
COPY app ./app

# по умолчанию запускаем только FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
