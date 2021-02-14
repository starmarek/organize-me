# OrganizeME :hospital: :date: :watch:
Web app that provides custom working schedule for a group of employees.
## Prerequisites
Before getting started you should have the following installed and running:
- [x] Docker - [instructions](https://docs.docker.com/engine/install/)
- [x] Docker-compose - [instructions](https://docs.docker.com/compose/install/)
- [x] Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)
- [x] Pipenv - [instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Development environment
### Clone

```
$ git clone https://gitlab.com/jaolejnik/organize-me.git
$ cd organize-me
```
### Run setup
```
$ ./admin.sh init
```
---

After a while you can check the containers/servers output:

The Vue application will be served from [`localhost:8080`](http://localhost:8080/) 
The Django API and static files will be served from [`localhost:8000`](http://localhost:8000/).

Proxy config in [`vue.config.js`](/vue.config.js) is used to route the requests
back to django's API on port 8000.

## Production environment

OrganizeME uses Heroku to run itself on a globally available server. `Procfile` and `app.json` are used to configure Heroku dynos and the startup of an app. The deployment itself, is handled by GitlabCI in the *heroku* job. For more info about CI/CD in the project, please read [CI/CD](#CI-CD).


### Static assets

App uses Django Whitenoise to serve all static files and Vue bundled files at `/static/`.
It allows us to skip Nginx (or similar Web server) setup and use a django WSGI server (*Gunicorn*) instead. Unfortunatelly this approach reduce the throughput and overall speed of an app. OrganizeME is created with the aim of a small group of people using it. 

If one would like to speed up the app there are two approaches:
- Incorporate CDN via Clodflare, AWS or similar.
- Switch from Whitenoise to a full-fledged web server.

For more details see [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/django.html).

## CI-CD

OrganizeME uses gitlab as a remote repository provider. Thanks to that, a marvelous gitlabCI is incorporated in the project. `.gitlabci.yml` is used to configure the CI pipeline. This pipeline is ran evetryime a change is pushed to the repository (regardless of a branch). The structure of a pipeline (stage / job) looks like that:

- build
  - install_pipenv
  - install_node 
- tests
  - flake8
  - black
  - isort
  - prettier
  - eslint
- deploy
  - heroku

The heroku job is configured to run only when a tag is pushed to a master branch.

For more details see [GitlabCI Documantation](https://docs.gitlab.com/ee/ci/README.html).

## Admin script
Automate common project maintenance tasks. You should always use it unless you really know what you are doing.

### Commands to use with admin script

*Project initialization*

Sets up containers, create your local pipenv, sets your pythonpath if you use vscode
``` 
$ ./admin.sh init
```
*Update core package versions*

In `.template.env` and in your `.env` you will find core package versions which are used in project. You should always update those versions with admin script since it makes sure to edit all needed config files. `pipenv` is the only package that you need to take care of yourself.
``` 
$ ./admin.sh update-yarn 2.4.0
$ ./admin.sh update-compose 3.8
$ ./admin.sh update-postgres 13.1
$ ./admin.sh update-python 3.9.1
$ ./admin.sh update-node 14.15.3
```
*Containers control*

Run containers detached and build images if they do not exists yet.
``` 
$ ./admin.sh containers-up
```
Build images.
``` 
$ ./admin.sh containers-build --cache=False
```
First build images, then run containers detached.
``` 
$ ./admin.sh containers-ground-up --cache=False
```
Show logs for given container (if no container passed -> whole compose cluster will be used)
``` 
$ ./admin.sh containers-logs django
```
*Packages control*

Manage both python and node packages that are used in project.
``` 
$ ./admin.sh install-pip numpy --dev
$ ./admin.sh install-yarn nodejs-timer --dev
$ ./admin.sh remove-pip django
$ ./admin.sh remove-yarn vue-cli
```