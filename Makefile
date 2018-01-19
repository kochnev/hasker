prod:
	#upgrade yum
	yum -y update
	yum -y install https://centos7.iuscommunity.org/ius-release.rpm

	#python3.6 and pip3.6
	yum -y install python36u
	yum -y install python36u-pip

        #django
	pip3.6 install django==1.11
	pip3.6 install django-debug-toolbar==1.9.1




