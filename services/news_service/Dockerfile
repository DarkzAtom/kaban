FROM python:3.11
WORKDIR /app
COPY requirements.txt .

# Install cron
RUN apt-get update && apt-get -y install cron

RUN pip install -r requirements.txt
COPY . .

COPY crontab /etc/cron.d/news-cron
RUN chmod 0644 /etc/cron.d/news-cron
RUN crontab /etc/cron.d/news-cron

# Create a script that runs both cron and your FastAPI app
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["/start.sh"]