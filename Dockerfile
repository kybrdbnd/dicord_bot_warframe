FROM python:3.8
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
#for logs
ENV PYTHONUNBUFFERED 1
CMD ["python", "bot.py"]