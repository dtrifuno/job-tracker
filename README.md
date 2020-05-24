# JobTracker

JobTracker is a web application that helps users create customized CVs and keep track of job application statuses, deadlines, descriptions and details for all positions that they have applied for during their job search.

Go to [trifunovski.me/jobtracker](https://trifunovski.me/jobtracker) to try it out!

![JobTracker](https://github.com/dtrifuno/job-tracker/blob/master/promo/profile.png?raw=true)

## Built With

### Backend (Python)

* [Flask web microframework](https://flask.palletsprojects.com/)
* [SQLAlchemy ORM](https://www.sqlalchemy.org/) 
* [Graphene](https://graphene-python.org/) 
* [Flask-GraphQL-Auth](https://github.com/NovemberOscar/Flask-GraphQL-Auth)

### Frontend (HTML/CSS/JavaScript)

* [Vue.js](https://vuejs.org/) (with the [Vuex state management library](https://vuex.vuejs.org/) and [vue-router](https://router.vuejs.org/))
* [Bootstrap](https://getbootstrap.com/) (with the [Bootswatch Lux](https://bootswatch.com/lux/) color theme for styling)
* [Apollo Link](https://www.apollographql.com/docs/link/) (a very low-level GraphQL client)
* [vue-notification](https://github.com/euvl/vue-notification)
* [vue-js-modal](https://github.com/euvl/vue-js-modal)

## Installation

This project uses [poetry](https://python-poetry.org/) for Python dependency management and the [Node package manager (npm)](https://www.npmjs.com/) for managing its JavaScript dependencies. Make sure that both are installed on your system, and then:

- Clone the repo.

```
$ git clone git@github.com:dtrifuno/job-tracker.git
```

- Setup the virtual environment and install the project's Python and Node dependencies.

```
$ cd job-tracker
$ poetry install
$ npm install
```

- Create a migrations folder, generate the initial migration and apply the migration to the development database.

```
$ poetry run create_dev_db
```

## Usage

### Development
Run 
```
$ poetry run dev
```
to start the Flask server in development mode, and
```
$ npm run serve
```
to start a client dev server.

By default, job-tracker's Flask development server is set up to run CORS only on `localhost/127.0.0.1`. Edit `config.py` if that is not the desired behavior.

### Deployment

For the rest of this section we will assume that we are trying to deploy JobTracker to a `/jobtracker` folder on an [Nginx web server](https://www.nginx.com/) and using a [PostgreSQL database](https://www.postgresql.org/). If that is not the case, you might need to edit `app/init.py` and `src/link.js` to change the API endpoints, and modify the supplied example configuration files.

#### Deploying the server
Clone the project and then run
```
$ poetry install
$ poetry add gunicorn psycopg2
```
to install the [Gunicorn WSGI Server](https://gunicorn.org/) and the [Psycopg PostgreSQL database adapter](https://pypi.org/project/psycopg2/). Create a file caled `.env` in the root project directory containing
```
FLASK_ENV = "production"
FLASK_DEBUG = "False"
SECRET_KEY = "<SOME_SECRET_KEY>"
JWT_SECRET_KEY = "<ANOTHER_SECRET_KEY>"
DATABASE_URI = "postgres://<DB_USERNAME>:<DB_PASSWORD>@<DB_HOSTNAME>:<DB_PORT>/<DB_NAME>"
```
where you should replace the text in the angle brackers with the correct values for your system (you can generate secret keys with the command `openssl rand -base64 32`)
and then create and apply the database migrations to the production database by running
```
$ poetry run create_prod_db
```

Create a [systemd](https://www.freedesktop.org/wiki/Software/systemd/) service to run the web application using Gunicorn (see sample `jobtracker.service` below, remember to modify the file paths to match those on your system).

```
[Unit]
Description=Gunicorn instance to serve jobtracker
After=network.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=dtrifuno
Group=www-data
WorkingDirectory=/home/dtrifuno/projects/job-tracker
Environment="PATH=/home/dtrifuno/.cache/pypoetry/virtualenvs/job-tracker-dnptnca1-py3.8/bin/"
EnvironmentFile=/home/dtrifuno/projects/job-tracker/.env
ExecStart=/home/dtrifuno/.cache/pypoetry/virtualenvs/job-tracker-dnptnca1-py3.8/bin/gunicorn --workers 4 --bind unix:jobtracker.sock -m 007 job_tracker:app
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
and then run
```
$ sudo systemctl start jobtracker
$ sudo systemctl enable jobtracker
```
to start it.

#### Deploying the client
Run
```
$ npm install
$ npm run build
```
to build a production ready version of the client, and the copy the contents of the newly created `dist/` folder to `jobtracker/` on your webserver to start serving the client. 

#### Routing API calls from Nginx to the application server
The only thing that's left is to setup proxying for API calls from our Nginx server to the Gunicorn application server, which is currently only accessible locally through a UNIX socket. For that, we use the following Nginx configuration file.
```
server {
    location = /jobtracker/graphql {
        include proxy_params;
        rewrite /jobtracker/graphql /graphql break;
        proxy_pass http://unix:/home/dtrifuno/projects/job-tracker/jobtracker.sock;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```
Remember to check the Nginx config file (`sudo nginx -t`) and then reboot the `nginx` service by running `sudo systemctl restart nginx`.


## TODO
* **Stats Dashboard**
Create a dashboard where users can keep track of the total number of applications submitted/rejected/waiting response/etc. and can set a goal for the number of submissions they want to make per month/week.
* **Calendar**
Create a page where the user can see all of their scheduled assessments, interviews and other upcoming deadlines. Integrate this functionality with Google Calendar.
* **Custom CV Sections**
The app is currently very opinionated about which sections to include in the CV (Education, Skills, Work History, ...) and in which order. Allow users to create custom sections and order them at will.
* **CV Themes**
Let users choose from a variety of CV stylings.
* **Authorization**
Job-tracker currently uses only basic JWT access tokens. Implement refresh tokens and server-side token invalidation after logout.
* **Testing**
Write unit and functional tests.
* **Containerize**
Package the application as a Docker container.

## License
[MIT](https://choosealicense.com/licenses/mit/)
