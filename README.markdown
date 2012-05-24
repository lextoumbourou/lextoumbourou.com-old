# The blog engine behind [LexToumbourou.com](http://lextoumbourou.com)

## Installation
* Clone project
```
cd ~/dev/
git clone git@github.com:lextoumbourou/and-stuff.git
```
* Create a new Django project
```
cd /srv/
sudo django-admin.py startproject TaxiDriverBlog .
chown you:www -r TaxiDriverBlog
```
* Configure Django settings.py with your database of choice (see Django docs for more info)
```
cd /srv/TaxiDriverBlog
vi settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'TaxiDriverBlog',
        'USER': 'travis',
        'PASSWORD': 'bickle',
        'HOST': '127.0.0.1',
        'PORT': '',
    } 
}

```
* Uncomment the admin site and add the blog module
```
INSTALLED_APPS = (
    ...

    'django.contrib.admin',
    'taxidriverblog.blog',
)
```
* Sync the database
```
python manage.py syncdb
```
## Usage
* Relies completely on the Django admin site, access it via http://www.taxidriverblog.com/admin
* Write what you know
* Show, don't tell

## License
MIT
