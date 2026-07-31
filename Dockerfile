FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as UID 1000, not root — matches the default first-user UID on both the
# dev machine and the deploy server, so any files the app writes stay owned
# by the host user instead of root on the bind-mounted volume.
RUN useradd -u 1000 -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "apartment_expense_bot.py"]
