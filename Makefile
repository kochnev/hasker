prod:
	#upgrade yum
	yum -y update
	yum -y install yum-utils
	yum -y groupinstall development

	#install python3.6 and pip
	yum -y install https://centos7.iuscommunity.org/ius-release.rpm
	yum -y install python36u
	yum -y install python36u-pip



