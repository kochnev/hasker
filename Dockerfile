FROM centos:7
RUN yum install -y git
RUN yum install -y make
RUN git clone https://github.com/kochnev/hasker.git
WORKDIR /hasker
