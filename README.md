

# Blog app




## Installation

Install my-project with npm

**Clone repository :**

```bash
git clone https://github.com/Shivahir2003/blogs_app.git
```
**Create virtualenvironment :**

```bash
python3 -m venv venv
```
**Activate virtualenvironment :**

```bash
source venv/bin/activate
```
**Open working directory :**

```bash
cd blogs_app/blogsite/
```
**Install dependencies :**

```bash
pip install -r requirements.txt
```
**makemigrations and start project:**

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```  
```bash
python manage.py runserver
```  

## Celery Tasks 

**start celery worker:**
```bash
celery -A blogsite worker -l info
```

**start celery beat:**

```bash
celery -A blogsite beat -l info
```

## Cronjob

**Add crontab:**
```bash
python manage.py crontab add
```
**Remove crontab:**
```bash
python manage.py crontab remove
```
**show all crontab:**
```bash
python manage.py crontab show
```


