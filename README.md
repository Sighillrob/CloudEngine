CloudEngine
===========

**Open source backend for mobile.**


Overview
=========

CloudEngine is an open source backend for building awesome mobile apps built using Python and django.
The aim of the project is to help mobile app developers get their apps off the ground
as quickly as possible. For this, CloudEngine provides basic services
required for building rich mobile apps out-of-the-box. The aim is also to create fully 
customizable and extensible framework for
building backend mobile services.


Requirements
=============
CloudEngine runs only on gunicorn server and hence currently runs only
on UNIX environments. For development purposes, you can use django's builtin webserver.

* Python (2.7.5+)
* Django (1.5.4+)
* MongoDB (2.4.6+)
* MySQL (5.5+)

All the python library dependencies are listed in `requirements.txt`

Installation
===============

It is recommended that you create a virtualenv namespace and activate it before installing
CloudEngine and its dependencies.

	virtualenv myenv
	cd myenv
	source bin/activate

You can install CloudEngine using pip. You can also grab the source distributions from the 
[project homepage][projectpage].

	pip install cloudengine	


Create a new django project (myproject)

	django-admin.py startproject myproject

Configure database and other necessary 
settings in your project's `settings.py`.

Add the following settings to `settings.py`
make sure your SECRET_KEY is a random secret string

	MONGO_HOST = 'localhost'   # assuming your mongodb server is running locally
	
	REST_FRAMEWORK = {
	    # Use hyperlinked styles by default.
	    # Only used if the `serializer_class` attribute is not set on a view.
	    'DEFAULT_AUTHENTICATION_CLASSES': (
	        'rest_framework.authentication.TokenAuthentication',
	        'rest_framework.authentication.SessionAuthentication',
	    ),
	    'DEFAULT_MODEL_SERIALIZER_CLASS':
	    'rest_framework.serializers.HyperlinkedModelSerializer',
	    'PAGINATE_BY': 10,
	
	    # Use Django's standard `django.contrib.auth` permissions,
	    # or allow read-only access for unauthenticated users.
	    'DEFAULT_PERMISSION_CLASSES': [
	        'rest_framework.permissions.IsAuthenticated',
	    ],
	    
	    DEFAULT_PARSER_CLASSES': (
	        'rest_framework.parsers.JSONParser',
	        'rest_framework.parsers.FormParser',
	        'rest_framework.parsers.MultiPartParser',
	        'rest_framework.parsers.FileUploadParser',
    	)
	}

	
	EMAIL_VERIFICATION_DAYS = 7
	
	PAGINATE_BY = 10
	

If you want to use Amazon S3 as your primary file storage service, also add the following settings and fill in your amazon credentials at appropriate places.

	# By default files are uploaded to amazon S3 buckets
	DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

	# The name of the directory that your app files will be uploaded to
	REMOTE_FILES_DIR = ''
	
	# AWS Credentials
	AWS_ACCESS_KEY_ID = ""
	AWS_SECRET_ACCESS_KEY = ""
	AWS_STORAGE_BUCKET_NAME = ""
	

In the list of `INSTALLED_APPS` add the following apps

	
	INSTALLED_APPS = (
	    	'django.contrib.auth',
	    	...
	    	...			
			'registration',
			'rest_framework',
			'rest_framework.authtoken',
			'storages',
			'cloudengine',
			'cloudengine.core',
			'cloudengine.classes',
			'cloudengine.push',
			'cloudengine.files',
			'cloudengine.users',
			)

Create database tables.

	python manage.py syncdb
	
Add the following line in the `myproject.urls.py`

	url('', include('cloudengine.urls')), 	
	
Run the gunicorn server with gevent-socketio worker class. Add the project directory 
to python path

	gunicorn -w 1 --pythonpath .  \
	--worker-class cloudengine.socketio.sgunicorn.GeventSocketIOWorker  \
	<your-project-wsgi-module>:application
	


On development environments, you can simply run the django development server

	python manage.py runserver

Please note the development server doesn't support SocketIO hence you can't test 
push notifications locally.
	
	
Technical Overview
====================

CloudEngine is a pure Python django stack. Each backend service is plugged in as django
app. Each service should be independently pluggable and usable except the core services. 
CloudEngine currently runs on gunicorn
server and hence runs only on UNIX environments. CloudEngine uses the excellent
[gevent-socketio][gevent-socketio] library for implementing real time communication
channels, which are the basis of current push notifications system. 
gevent-socketio is the python port of the popular [socket.io][socket.io] library. 
For storage we use a combination of relational database (MySQL/ PostgreSQL) and a
NoSQL db (Currently mongodb). CloudEngine uses [django-rest-framework][django-rest] for providing
REST interfaces to services.


Client libraries
==================

The aim of the project is also to provide readily available client libraries for 
as many different platforms as possible to make it easier to consume CloudEngine
services on mobile devices.
Currently only Android SDK is available at -  [https://github.com/cloudengine/Android-SDK][android-sdk]
We plan to add SDKs for more platforms 


Documentation & Support
========================

Complete documentation is available at - ?

For discussions, questions and support use the [CloudEngine discussion group][group]

or [Github issue tracking][issue-tracker]

You may also want to [follow the authors on twitter] [twitter]. 



License
========
See the LICENSE file for more info.



[twitter]: https://twitter.com/thecloudengine
[group]: https://groups.google.com/forum/#!forum/cloudengine-dev
[gevent-socketio]: https://github.com/abourget/gevent-socketio
[socket.io]: http://socket.io
[issue-tracker]: https://github.com/cloudengine/CloudEngine/issues
[android-sdk]: https://github.com/cloudengine/Android-SDK
[django-rest]: https://github.com/tomchristie/django-rest-framework
[projectpage]: http://getcloudengine.com
