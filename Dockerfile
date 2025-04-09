FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y software-properties-common && \
    apt-get install -y build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev libfreetype6-dev libmysqlclient-dev libpq-dev libcurl4-openssl-dev libsqlite3-dev git wget curl flang

RUN apt-get install -y gfortran pkg-config libblas-dev liblapack-dev libatlas-base-dev
RUN wget https://www.python.org/ftp/python/3.11.12/Python-3.11.12.tgz
RUN tar -xvf Python-3.11.12.tgz
RUN cd Python-3.11.12 && ./configure --enable-optimizations && make -j4 && make install
RUN python3.11 -m pip install tinydb 'tensorflow[and-cuda]' langchain langchain-openai gensim flask_wtf python-docx legacy-cgi flask_mail pycryptodome librosa flask_login openpyxl xlwt geopandas opencv-python chardet pyquery rsa openpyxl soundfile chardet statsmodels python-levenshtein nltk lxml keras flask seaborn wordcloud

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]