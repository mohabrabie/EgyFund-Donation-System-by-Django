FROM python:3.8
ENV EMAIL_HOST_VALUE="smtp.gmail.com"
ARG host_user = 'mohab@gmail.com'
ARG host_passwd = ''
ARG admin_username="admin"
ARG admin_pass="egyfund"
ARG admin_email=$host_user
WORKDIR /usr/src/egyfundapp
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
COPY .env egyfund/.env
RUN python manage.py makemigrations \ 
    && python manage.py migrate \
    && python manage.py createsuperuser_if_none_exists --user=$admin_username --password=$admin_pass --email=$admin_email
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
