prod:
	#upgrade yum
	yum -y update
	yum -y install https://centos7.iuscommunity.org/ius-release.rpm
	yum -y install sudo

	#python3.6 and pip3.6
	yum -y install python36u
	yum -y install python36u-pip
       
        #django
	pip3.6 install django==1.11
	pip3.6 install django-debug-toolbar==1.9.1
        
	#psycopg2
	pip3.6 install psycopg2
	
	#postgresql
	yum install -y postgresql-server postgresql-contrib
	sudo -u postgres /usr/bin/initdb /var/lib/pgsql/data/
	sudo -u postgres /usr/bin/pg_ctl start  -D /var/lib/pgsql/data -s -o "-p 5432" -w -t 300
	
	#create user and database
	sudo -u postgres psql -f postgresql/init.sql

        #init django project
	python3.6 manage.py collectstatic
	python3.6 manage.py migrate

	#nginx
	yum -y install nginx
	cp /hasker/nginx/nginx_hasker.conf /etc/nginx/conf.d/
	nginx
		
        #uwsgi
	yum -y install python36u-devel
	yum -y install gcc
	pip3.6 install uwsgi
	uwsgi --ini /hasker/uwsgi/uwsgi.ini
