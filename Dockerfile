FROM python:3
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN useradd -m appuser
USER appuser
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]