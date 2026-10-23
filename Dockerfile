FROM python:3.11-slim

# Install postgresql, cron, and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    postgresql-contrib \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Install Python requirements for app and smsgw
COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt "werkzeug<3.0"

# Copy project files
COPY app /app
COPY smsgw /smsgw
COPY seed /seed
COPY start.sh /start.sh

RUN chmod +x /start.sh \
    && mkdir -p /var/sewasetu/uploads /var/log/sewasetu \
    && crontab /app/deploy/crontab

EXPOSE 8000

CMD ["/start.sh"]
