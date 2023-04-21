# Create Web/Api/Worker with Nuxt/Vuetify and deploy to Render.com

## Create Webapp
```
$ yarn create nuxt-app webapp
create-nuxt-app v5.0.0
✨  Generating Nuxt.js project in .
? Project name: render-deploy-web
? Programming language: JavaScript
? Package manager: Yarn
? UI framework: Vuetify.js
? Template engine: HTML
? Nuxt.js modules: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Linting tools: ESLint
? Testing framework: Jest
? Rendering mode: Single Page App
? Deployment target: Static (Static/Jamstack hosting)
? Development tools: jsconfig.json (Recommended for VS Code if you're not using typescript)
? Continuous integration: None
? Version control system: Git
```

## Create API
```
$ mkdir api && cd "$_"
$ mkvirtualenv [appname]-api
$ pip install flask flask_jwt_extended flask_limiter flask_cors marshmallow celery redis gunicorn openai
$ pip freeze > requirements.txt
$ curl https://raw.githubusercontent.com/render-examples/celery/master/app.py --output app.py
```

## Create Worker
```
$ mkdir worker && cd "$_"
$ mkvirtualenv [appname]-worker
$ pip install openai celery flower gunicorn redis flask-cors tasks
$ pip freeze > requirements.txt
$ curl https://raw.githubusercontent.com/render-examples/celery/master/tasks.py --output tasks.py
```

## Create render.yaml
https://github.com/render-examples/celery/blob/master/render.yaml
```
services:
  - type: worker
    name: queue
    region: oregon
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "celery --app tasks worker --loglevel info --concurrency 4"
    autoDeploy: false
    envVars:
      - key: CELERY_BROKER_URL
        fromService:
          name: app-celery-redis
          type: redis
          property: connectionString
  - type: web
    name: app
    region: oregon
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
    autoDeploy: false
    domains:
      - domain: api.example.com
        ssl: true
    envVars:
      - key: CELERY_BROKER_URL
        fromService:
          name: celery-redis
          type: redis
          property: connectionString
  - type: web
    name: app
    region: oregon
    env: static
    buildCommand: "yarn; yarn build"
    startCommand: "yarn start"
    autoDeploy: false
    domains:
      - domain: example.com
        ssl: true
  - type: redis
    name: celery-redis
    region: ohio
    plan: starter # we choose a plan with persistence to ensure tasks are not lost upon restart
    maxmemoryPolicy: noeviction # recommended policy for queues
    ipAllowList: [] # only allow internal connections
```

## Create repo and push to github
```
```

## Create render.com service and deploy
```
```

