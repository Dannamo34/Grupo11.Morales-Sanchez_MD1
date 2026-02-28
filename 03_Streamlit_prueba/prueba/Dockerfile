FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD [streamlit, run, dashboard.py, --server.address=0.0.0.0, --server.port=8501]
