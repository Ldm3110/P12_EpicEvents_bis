# P12_EpicEvents_bis
Develop a securized Back-End architecture using Django Orm 

## 1. Cloning and Install the virtual environment

- Cloning the repository :
```
$ git clone https://github.com/Ldm3110/P12_EpicEvents_bis.git
```

- Go to the new folder and create virtual environment :
```
$ cd P12_EpicEvents_bis/
$ python3 -m venv env 
```

- Activate the virtual environment :
```
$ source env/bin/activate
```

## 2. Initialize the project

### Database

- Install PostgreSQL :

This project used a PostgreSQL database, if you don't have already on your local machine you must
install it. Go to the following adress 

https://www.postgresql.org/

and follow the installation instructions

- Create your .env folder :

You may have a folder named ```$ .env``` on the project to initialize the database. For it, please follow the instructions
below :

1. Go at the racine of the project : ```$ cd EpicEvents/```


2. In this directory you have access to a folder named ``` $ .env.example ```. Open this folder, copy the content and
create a new folder named ```$ .env```


3. Now paste the contents of this file and replace all the information with the information about the database you have created


4. Saved your new folder. Congratulation you have initialize your database

### Requirements

- You must install all the requirements of the project, type the following command :
```
$ pip install -r requirements.txt
```

## 3. Basic information

To run the project you will need to migrate all the project informations on your database. To proceed type the following command

```
$ ./manage.py makemigrations
$ ./manage.py migrate
```

To access at the django admin interface you will need to create a superuser (member of the Management Team), type the commands :

```
$ ./manage.py createsuperuser
```

You will need to fill in the following information : 
- the username
- the password

(Note that the email is not required)


## Using the API

Refer to the API documentation at the following address :

"Adress Postman"