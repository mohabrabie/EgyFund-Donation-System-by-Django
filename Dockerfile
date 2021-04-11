FROM python:3.8
ENV EMAIL_HOST_VALUE="smtp.gmail.com"
ARG host_user
ARG host_passwd
WORKDIR /usr/src/egyfundapp
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN echo "EMAIL_HOST=\"$EMAIL_HOST_VALUE\"\nEMAIL_HOST_USER=\"$host_user\"\nEMAIL_HOST_PASSWORD=\"$host_passwd\"\n" > egyfund/.env
RUN python manage.py makemigrations \ 
    && python manage.py migrate
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
