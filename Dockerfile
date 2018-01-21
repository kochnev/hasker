FROM centos:7
RUN yum install -y git
RUN yum install -y make
#RUN yum install -y initscripts && yum clean all
EXPOSE 80
