prod:
	#upgrade yum
	yum -y update
	yum -y install https://repo.ius.io/ius-release-el7.rpm
	yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
	yum -y install sudo

	#python3.6 and pip3.6
	yum -y install python36u
	yum -y install python36u-pip
    pip3.6 install --upgrade pip

       
    #django
    pip3.6 install django==1.11
	pip3.6 install django-debug-toolbar==1.9.1
        
    #psycopg2
    yum groupinstall 'Development Tools' -y
    yum install python3-devel -y
    yum install postgresql-libs -y
    yum install postgresql-devel -y
    pip3.6 install psycopg2
    pip3.6 install Pillow

	#postgresql
	yum install -y postgresql-server postgresql-contrib
	sudo -u postgres /usr/bin/initdb /var/lib/pgsql/data/
	sudo -u postgres /usr/bin/pg_ctl start  -D /var/lib/pgsql/data -s -o "-p 5432" -w -t 300
	
	#create user and database
	sudo -u postgres psql -f postgresql/init.sql -v db_user=${DB_USER} -v db_name=${DB_NAME} -v db_password=${DB_PASSWORD}

        #init django project
	python3.6 manage.py collectstatic --noinput
	python3.6 manage.py makemigrations
	python3.6 manage.py migrate

	#nginx
	yum -y install nginx
	cp /hasker/nginx/nginx_hasker.conf /etc/nginx/conf.d/
	nginx
		
    #uwsgi
	pip3.6 install uwsgi
	uwsgi --ini /hasker/uwsgi/uwsgi.ini
