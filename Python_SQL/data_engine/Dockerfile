FROM python:3.10-slim

WORKDIR /app

# 1. Update this line to point to the file inside for_docker
COPY for_docker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 2. Update this line to point to the script in the parent folder
# (Since context is '..', we just refer to it by name)
COPY update_DB.py .

CMD ["python", "update_DB.py"]