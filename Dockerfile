FROM centos:7
RUN yum install -y git make

#upgrade yum
RUN yum -y update
RUN yum -y install https://repo.ius.io/ius-release-el7.rpm
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install sudo

#for development only
ENV SECRET_KEY 'n3px@&(72w%=#a95z7yoxze96_3_)_(l(obywpw#ll(+2qzob('
ENV DB_USER hasker_admin
ENV DB_NAME hasker
ENV DB_PASSWORD 123456789
ENV DB_HOST 127.0.0.1
ENV DB_PORT 5432
ENV LANG en_US.UTF-8
EXPOSE 80
