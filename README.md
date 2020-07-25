# **Keto Tracker**

Keto Tracker is a full stack Web application that allows users to create an account, log in, look up the nutrition of foods, and record the foods eaten and the day. 

The application has 93% test coverage using Python unittest.


### Contents

* [Tech stack](#techstack)
* [Installation](#installation)
* [Features](#features)
* [About The Developer](#aboutme)

## <a name="techstack"></a>Technologies

Tech Stack: Python, JavaScript, HTML, CSS, Flask, Jinja, PostgreSQL, SQLAlchemy, Bootstrap, unittest <br>
APIs: Edam food database 

### Prerequisites

- PostgreSQL
- Python 3.x
- API key for Edam


### <a name="installation"></a>Run Keto Tracker on your computer

Clone or fork repository:
```
$ git clone https://https://github.com/EpicRowan/Keto_tracker
```
Create and activate a virtual environment inside your Keto Tracker directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Add your API key into the header scripts templates/homepage.html line 79

Create database 'carbs':
```
$ createdb carbs
```
Run model.py interactively in the terminal, and create database tables:
```
$ python3 -i model.py
>>> db.create_all()
>>> quit()

```
Run seed.py to load all of the data into the newly created and setup database
```
$ python3 seed.py
```
Run the app from the command line.
```
$ python3 server.py
```

## <a name="features"></a>Features

### **Register and Login**
<img src="/static/img/login.png" width="1000" height="200">

Create a new account and log in to your account to save your entries in the database

### **Search**


<!-- 
<img src="/static/img/help_tips.gif" width="1000" height="500"> -->

### **Browse food**

fdfd

### **Record food and date**

jjkjk

<img src="/static/img/new_entry.png" width="1000" height="500">



## <a name="aboutme"></a>About the Developer

 Doom Mapper was created by former teacher Rowan Shepherd, a science and dark humor enthusiast who transitioned into software engineering. This is her first fullstack project. She can be found on [LinkedIn](https://https://www.linkedin.com/in/rowan-shepherd/) and on [Github](https://github.com/EpicRowan).
