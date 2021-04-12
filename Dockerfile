FROM python:3.8
ENV EMAIL_HOST_VALUE="smtp.gmail.com"
WORKDIR /usr/src/egyfundapp
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN python manage.py makemigrations \ 
    && python manage.py migrate 
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
