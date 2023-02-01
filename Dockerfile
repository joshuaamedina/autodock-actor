# pull base image
FROM sd2e/reactors:python3


# add requirements.txt to docker container
ADD requirements.txt /requirements.txt

# install requirements.txt
RUN pip3 install -r /requirements.txt

# add the python script to docker container
ADD reactor.py /reactor.py

# command to run the python script
CMD ["python3", "/reactor.py"]
