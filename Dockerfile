FROM python
LABEL maintainer="Bontchev"
LABEL name="ipphoney"
LABEL version="1.0.0"
EXPOSE 631
COPY . /ipphoney/
WORKDIR /ipphoney
RUN pip install -r requirements.txt
CMD [ "python", "./ipphoney.py" ]
