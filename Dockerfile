FROM python:3.13.3-slim-bookworm

ADD src /app/
ADD requirements.txt /app/
ADD bench.py /app/
WORKDIR /app
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]