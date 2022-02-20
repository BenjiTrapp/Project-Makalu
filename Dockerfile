FROM python:3.4-alpine
LABEL maintainer="Nyctophobia <benji.trapp@gmail.com>" \
      org.label-schema.name="Project Makalu" \
      org.label-schema.description="An unsecure Webshop with an intentional broken Session Handling" \
      org.label-schema.docker.cmd="docker run --rm -p 4711:4711 nyctophobia/project-makalu" \
      org.label-schema.vcs-url="https://github.com/BenjiTrapp/Project-Makalu" 


COPY . /code
COPY static /code/static
COPY templates /code/templates
WORKDIR /code

RUN pip3 install -r requirements.txt

EXPOSE 4711
ENTRYPOINT ["python", "ProjectMakaluApp.py"]