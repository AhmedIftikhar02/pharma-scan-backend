# 1. Official lightweight Python image use karenge
FROM python:3.11-slim

# 2. Container ke andar working directory set karenge
WORKDIR /code

# 3. requirements.txt ko copy karke dependencies install karenge
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Pura pharma_scan folder container mien copy karenge
COPY ./pharma_scan /code/pharma_scan

# 5. Hugging Face Spaces ke liye permissions handle karna (Zaroori step)
RUN chmod -R 777 /code

# 6. Port 7860 use hota hai Hugging Face par, server start karne ki command
CMD ["uvicorn", "pharma_scan.main:app", "--host", "0.0.0.0", "--port", "7860"]