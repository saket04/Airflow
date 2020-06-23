FROM python:alpine3.7
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "application.py" ]
ENTRYPOINT [ "python" ]
