# Legal Attest Letter Generator - Taiwan 台灣郵局存證信函產生器 #

A tool for creating a legal attest letter of Taiwan - in PDF format.

This repo forked from [csterryliu](https://github.com/csterryliu/Legal-Attest-Letter-Generator-TW). It copies some approaches from [his web build](https://github.com/csterryliu/Legal-Attest-Letter-Generator-TW-Django)
Becasue there are minor changes that may break the original repository, so here it is.

![sample](./img/sample.png)

## Feature ##

- 輸出整齊、美觀的信函  
  The output is neat and beautiful.  

- 可指定任意數目之姓名、地址  
  You can specify any number of names or addresses.  

- 可排版：只需用純文字編輯器打好內容並排版，便會反應至信函上，使內容不至於擁擠  
  Support indentation: The only thing you have to do is typing your main article and indenting them on a text editor. The output will reflect your indentation so that the main article won't look crowded.  

## How To Use It ##

### get source code ###

Download or `git clone` this repository.

### Run Locally ###

#### Prerequisite ####

pip3(install w/ python3), [python3](https://www.python.org/downloads/)

*In Debian,
`$ sudo apt install python3 python3-pip python3-venv`
(optional) set python 3.7 to default toolchain with `$ update-alternatives`

(for development only)
`$ git clone ${this-repo}`
`$ python -m venv venv`
`$ source venv/bin/activate`

change directory into the source code folder.

#### install dependencies ####

choose which one you want to use, and `$ pip install -r src/requrements.txt -r src/requirements-server.txt`

    - run command line tool
`$ python src/cli.py`
    - run GUI (great for users)
`$ python src/gui.py`
    - run as JSON API server
`$ python src/server/server.py`
OR
`$ gunicorn server:app`

### run with containers (docker) ###

containers are great for those who don't want to install dependencies in your own computer.

1. Prerequisite
[git](https://git-scm.com/), [docker](https://docs.docker.com/install/) CE, w/ any container runtime

2. Build your image
You can build your image locally, or build in your flavor environment, such as GCP. You must to have one if your choose the later choice.

    - local build
    (with docker build)
    `docker image build --tag=legal-attest-letter-generator --file=Dockerfile-${type} .`

    - remote build
    (with cloud build, you should have a GCP project)
    `gcloud builds submit . --config=cloudbuild.yaml`

3. Run

Despite how your build your containers, or just don't want to build yourself, you can pull one with `$ docker image pull ...`, and then run with `$ docker container run --rm ${your image}`

#### some notes for containers ####

- CLI build
use `docker container run --rm -v ${pwd}/outputFolder:/tmp/pdfs -v ${input}:/tmp/input --senderName abc --senderAddr lorem ...... /tmp/input` to mount your file ins-and-outs of a container. You could also use `docker volume` that you can manage your outputs yourself.

- GUI build
you need to set DISPLAY for your container and mount X11. see [docker-tkinter-tclerror-couldnt-connect-to-display](https://stackoverflow.com/questions/49169055/docker-tkinter-tclerror-couldnt-connect-to-display?rq=1)

- Web server build
Use `docker container run -p ....` to expose your container with a real localhost port.
It consumes an `application/json` object:

    {
        config:{
            senders:[ person_Object ],
            receivers: [ person_Object ],
            carbonCopy: [ person_Object ]
        },
        content: {
            data: "base64 encoded data string"
        }
    }

while a `person` is

    {
        name: "string",
        address "string"
    }

## Extra Dependencies ##

These are assets not as libraries.

- [Letter sample provided by Post Office of Taiwan](http://www.post.gov.tw/post/internet/Download/index.jsp?ID=220301)
- [Traditional Chinese font provided by National Development Council, Taiwan](http://data.gov.tw/node/5961)
