Hsker: Poor Man's Stackoverflow
=====================

It is a simple Q&A web application written on Django 1.11.

## Stack of technologies ##

* CentOS 7
* Python 3.6
* Nginx 
* uWSGI 
* Django 1.11
* django-debug-toolbar 1.9.1
* PostgreSQL 
* Twitter Bootstrap
* Javascript, jQuery

## Prerequisites

   You have to have Docker on your computer to build image and run a container.

## Installing

* `docker build -t hasker .`
* `docker run --rm -it -p 8000:80 hasker`
* `git clone https://github/kochnev/hasker.git` 
* `cd hasker`
* `make prod`

Then the web application will be available by address
http://localhost:8000/

## License

This project is licensed under the MIT License
