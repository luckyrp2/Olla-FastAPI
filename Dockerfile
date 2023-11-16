# 
FROM python:3.9

# 
WORKDIR /app

# 
COPY requirements.txt .

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY . .

# 
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]


# can build using docker build -t olla-app