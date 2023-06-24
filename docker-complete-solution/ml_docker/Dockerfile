FROM ultralytics/ultralytics:latest-arm64
ADD ./*.py /usr/src/app/
ADD ./*.sh /usr/src/app/
ADD ./*.yaml /usr/src/app/
ADD ./*.pt /usr/src/datasets/
ADD ./supervisor.conf /etc/supervisor/conf.d/
RUN apt-get -y update
RUN apt-get -y install supervisor
RUN pip install paho-mqtt pathlib ultralytics
RUN chmod +x  /usr/src/app/ml.sh
RUN ln -s /usr/bin/python3 /usr/bin/python


WORKDIR /usr/src/app

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
