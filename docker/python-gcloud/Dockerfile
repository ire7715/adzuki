FROM python:3.6

RUN curl -s https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-218.0.0-linux-x86_64.tar.gz | \
    tar -xz -C /tmp/ && \
    bash /tmp/google-cloud-sdk/install.sh --quiet --rc-path /root/.bashrc

COPY bootstrap.sh /etc/bootstrap.sh

CMD ["/bin/bash"]
