FROM python:3.9-buster

COPY . /dirstatstocloudwatch

RUN pip install -U pip
RUN pip install boto3
RUN pip install -r dirstatstocloudwatch/requirements.txt

ENTRYPOINT [ "python", "/dirstatstocloudwatch/dirstatstocloudwatch/main.py"]
CMD ["-c=dirstatstocloudwatch/configs/your-config-file-name-here.yaml"]
