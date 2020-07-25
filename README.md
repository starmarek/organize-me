# OrganizeME :hospital: :date: :watch:

Vue and Django are clearly separated in this project. Vue, Yarn and Webpack handles all frontend logic and bundling assessments. Django and Django REST framework to manage Data Models, Web API and serve static files.

Django is primarily used for the backend, and have view rendering and routing handled by Vue + Vue Router as a Single Page Application (SPA).

Django serve the application entry point (`index.html` + bundled assets) at `/` ,
data at `/api/`, and static files at `/static/`. Django admin panel is also available at `/admin/` and can be extended as needed.


### Includes

- Django
- Django REST framework
- Django Whitenoise, CDN Ready
- Vue CLI 3
- Vue Router
- Vuex
- Gunicorn
- Configuration for Heroku Deployment

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
- [x] Docker - [instructions](https://yarnpkg.com/en/docs/install)
- [x] Docker-compose - [instructions](https://yarnpkg.com/en/docs/install)
### Optional (Mostly for extra debug options)
- [x] Yarn - [instructions](https://yarnpkg.com/en/docs/install)
- [x] Vue CLI 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [x] Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)
- [x] Pipenv - [instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Setup
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

### Not-in-container setup (optional dependencies required)

```
$ yarn install
$ pipenv install --dev && pipenv shell
$ python manage.py migrate
```

#### Running bare development servers

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

The dual dev server setup allows you to take advantage of
webpack's development server with hot module replacement.
Proxy config in [`vue.config.js`](/vue.config.js) is used to route the requests
back to django's API on port 8000.

## Static Assets

See `settings.dev` and [`vue.config.js`](/vue.config.js) for notes on static assets strategy.

We implement the approach suggested by Whitenoise Django.
For more details see [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/django.html)

It uses Django Whitenoise to serve all static files and Vue bundled files at `/static/`.
