#
#                                 - [ BROAD'21 ] -
#
# A docker instance for accessing AWS resources
# This wraps the cellprofiler docker registry
#


FROM fiji/fiji:fiji-openjdk-8

USER root

# Install S3FS 

RUN apt-get -y update           && \
    apt-get -y upgrade          && \
    apt-get -y install 		\
	automake 		\
	autotools-dev 		\
	g++ 			\
	git 			\
	libcurl4-gnutls-dev 	\
	libfuse-dev 		\
	libssl-dev 		\
	libxml2-dev 		\
	make pkg-config		\
	sysstat			\
	curl

WORKDIR /usr/local/src
RUN git clone https://github.com/s3fs-fuse/s3fs-fuse.git
WORKDIR /usr/local/src/s3fs-fuse
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

RUN apt-get -y install software-properties-common python3-pip

# Install AWS CLI

RUN pip3 install awscli 

# Install boto3

RUN pip3 install boto3

# Install watchtower for logging

RUN pip3 install watchtower

# Install pandas for optional file downloading

RUN pip3 install pandas

# SETUP NEW ENTRYPOINT

WORKDIR /opt/fiji
COPY fiji-worker.py .
COPY instance-monitor.py .
COPY run-worker.sh .
RUN chmod 755 run-worker.sh

ENTRYPOINT ["./run-worker.sh"]
CMD [""]

