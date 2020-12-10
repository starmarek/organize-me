# OrganizeME :hospital: :date: :watch:

Vue and Django are clearly separated in this project. Vue, Yarn and Webpack handles all frontend logic and bundling assessments. Django and Django REST framework to manage Data Models, Web API and serve static files.

Django is primarily used for the backend, and have view rendering and routing handled by Vue + Vue Router as a Single Page Application (SPA).

Django serve the application entry point (`index.html` + bundled assets) at `/` ,
data at `/api/`, and static files at `/static/`. Django admin panel is also available at `/admin/`.


### Includes

- Django
- Django REST framework
- Django Whitenoise
- Vue CLI 3
- Vue Router
- Vuex
- Gunicorn
- Configuration for Heroku Deployment
- Configuration for GitlabCI CI/CD
- Docker for development environment

### Structure

| Location             | Content                                           |
| -------------------- | ------------------------------------------------- |
| `/backend`           | Django Project & Backend Config                   |
| `/backend/api`       | Django App (`/api`)                               |
| `/src`               | Vue App                                           |
| `/src/main.js`       | JS Application Entry Point                        |
| `/public/index.html` | Html Application Entry Point (`/`)                |
| `/public/static`     | Static Assets                                     |
| `/dist/`             | Bundled Assets Output (generated at `yarn build`) |

## Prerequisites

Before getting started you should have the following installed and running:

### Must-have
- [x] Docker - [instructions](https://docs.docker.com/engine/install/)
- [x] Docker-compose - [instructions](https://docs.docker.com/compose/install/)
### Optional (Extra debug options or undockerized development env)
- [x] Yarn - [instructions](https://yarnpkg.com/en/docs/install)
- [x] Vue CLI 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [x] Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)
- [x] Pipenv - [instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Development environment
### Clone

```
$ git clone https://gitlab.com/jaolejnik/organize-me.git
$ cd organize-me
```

### Run Docker development containers


```
$ docker-compose up -d
```


#### Useful docker commands and flags

Remove orphan containers (when you change name of the container in the docker-compose.yml):

```
$ docker-compose up (...) --remove-orphans
```

Force rebuild of the container images:

```
$ docker-compose up (...) --build
```

Lookup the logs from containers:

```
$ docker-compose logs -f
```
Check actually running containers:

```
$ docker ps
```

Run command in chosen container:

```
$ docker-compose exec <container-name> <command>
```
Run bash shell in the container:

```
$ docker-compose exec <container-name> bash
```

### Undockerized setup (optional dependencies required)

```
$ yarn install
$ pipenv install --dev && pipenv shell
$ python manage.py migrate
```

#### Run bare development servers

```
$ python manage.py runserver
```

From another tab in the same directory:

```
$ yarn serve
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
  - build 
- tests
  - test_pytest
  - test_dummy
- deploy
  - heroku

The heroku job is configured to run only when a change is pushed to a master branch.

For more details see [GitlabCI Documantation](https://docs.gitlab.com/ee/ci/README.html).
