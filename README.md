# EgyFund-Donation-System-by-Django
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)

> Crowdfunding is the use of small amounts of capital from a large number of individuals to finance a new business venture, typically via the Internet.
Crowdfunding is a form of crowdsourcing and alternative finance. It provides a forum to anyone with an idea to pitch it in front of waiting investors. 


## Aim of the project
Create a web platform for starting fundraise
projects in Egypt.
![alt-text](https://github.com/mohabrabie/EgyFund-Donation-System-by-Django/blob/74d51eceffbd4380f4d9b53a450b1d42d3ae0b70/ezgif.com-gif-maker.gif)

## Features of the project
1- User :
##### Authentication System​ :
- Registration:
- Activation Email after registration
- Once the user register he should receive an email with the activation link. The user shouldn’t be able to login without
activation. The activation link should expire after 24 hours.
- Login
- The user should be able to login after activation using his email
and password

####  profile :
- User can view his profile
- User can view his projects
- User can view his donations
- User can edit all his data except for the email
- User can have extra optional info other than the info he added
while registration (Birthdate, facebook profile, country)
- User can delete his account (Note that there must be a
confirmation message before deleting)

2- project 
- The user can create a project fund raise campaign 
- Users can view any project and donate to the total target

- Users can add comments on the projects

- Users can report inappropriate projects

- Users can report inappropriate comments
- Users can rate the projects
- Project creator can cancel the project if the donations are less than
25% of the target

3- Homepage
A slider to show highest five rated running projects
List of the latest 5 projects
A list of the categories.User can open each category to view its projects
Search bar tht enables users to search projects by title or tag

## Installation

```sh
OS: Cross Platform
```
```sh
IDEs Recommended: VSCode or IntelliJ
```
## Development setup
install virtualenv  then activate it and install all dependences which in requirements.txt


```sh
pip3 install -r requirements.txt
```

```sh
Create .env file 
```
```sh
python3 manage.py makemigrations
```
```sh
python3 manage.py migrate
```
```sh
python3 manage.py runserver
```

## To Build an image and run it type the following commands:

### Docker commands: (Host user and host password are related to the email confirmation link "GMAIL RECOMMENDED")
1- Build your image:
```sh
docker build --build-arg host_user="YOUR EMAIL"[REQUIRED] --build-arg host_passwd="YOUR PASSWORD"[REQUIRED] --build-arg admin_username="YOUR USERNAME"[OPTIONAL] --build-arg admin_pass="YOUR PASSWORD"[OPTIONAL] --build-arg admin_email="YOUR EMAIL"[OPTIONAL] -t egyfund:v1.0.0
```
Sample: 
```sh
docker build --build-arg host_user=aegyfund@gmail.com --build-arg host_passwd=R503abc! --build-arg admin_username=admin --build-arg admin_pass=egyfund --build-arg admin_email=shehab33@yahoo.com -t egyfund:v1.0.0 .
```
2- Run your container:
```sh
docker run -d -p 8081:8000 --name=egyfund egyfund:v1.0.0
```

## Note: 
If you are going to provide your own host email you have set less secure app to true in https://www.google.com/settings/security/lesssecureapps

# Contributers
- Ahmed Khaled.
- Mostafa Mowaad.
- Shehab El Deen Alalkamy.
- Mohab Rabie.
- Amed Zakaria.
