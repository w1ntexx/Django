## Manual Build
> 👉 Download the code
```bash
$ git clone https://github.com/w1ntexx/Django.git
$ cd sitetimix
```

<br />

> 👉 Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

Runs with [livereload](https://github.com/tjwalch/django-livereload-server/)

```bash
$ python manage.py livereload
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`

<br />

## Codebase structure
```bash
< PROJECT ROOT >
   |
   |-- sitetimix/                              
   |    |-- settings.py 
   |    |-- urls.py
   |
   |-- cats/
   |    |-- views.py
   |    |-- admin.py
   |    |-- urls.py
   |    |-- models.py
   |    |-- tests.py
   |    |-- templates/
   |         |-- cats/
   |              |-- index.html      
   |    |-- templatetags/     
   |         |-- cat_tags.py
   |     
   |-- users/
   |    |-- views.py
   |    |-- admin.py
   |    |-- urls.py
   |    |-- models.py
   |    |-- tests.py
   |    |-- context_processors.py
   |    |-- authentication.py
   |    |-- templates/
   |         |-- users/
   |              |-- profile.html     
   |
   |-- templates/
   |         |-- base.html
   |
   |-- media/
   |    |-- photos/
   |    |-- social-auth/
   |    |-- users/
   |
   |-- requirements.txt
   |
   |-- manage.py
   |
   |-- ************************************************************************
```

<br />
