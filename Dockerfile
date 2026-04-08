FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# Overwrite the default to run the minimal inference server for Phase 1
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860"]
