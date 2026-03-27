FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY build_info_app.py .

ARG BUILD_COMMIT=unknown
ARG BUILD_USER=unknown
ARG BUILD_TIME=unknown

ENV BUILD_COMMIT=${BUILD_COMMIT}
ENV BUILD_USER=${BUILD_USER}
ENV BUILD_TIME=${BUILD_TIME}

EXPOSE 5000
CMD ["python", "build_info_app.py"]
