# JobTracker

JobTracker is a web application that helps users create customized CVs and keep track of job application statuses, deadlines, descriptions and details for all positions that the user has applied for during their job search.

Go to [trifunovski.me/job-tracker](https://trifunovski/me/job-tracker) to try it out!

![JobTracker](https://github.com/dtrifuno/job-tracker/blob/master/src/assets/job-tracker.png?raw=true)

## Built With

### Backend (Python)

* [Flask web microframework](https://flask.palletsprojects.com/)
* [SQLAlchemy ORM](https://www.sqlalchemy.org/) 
* [Graphene](https://graphene-python.org/) 

### Frontend (HTML/CSS/JavaScript)

* [Vue.js](https://vuejs.org/) (with [Vuex state management library](https://vuex.vuejs.org/) and [vue-router](https://router.vuejs.org/))
* [Bootstrap](https://getbootstrap.com/) (with the [Bootswatch Lux](https://bootswatch.com/lux/) color theme for styling)
* [Apollo Link](https://www.apollographql.com/docs/link/)
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

By default, the job-tracker's Flask development server will run CORS only on `localhost/127.0.0.1`. Edit `config.py` if that is not the desired behavior.

### Deployment

## TODO
* **Stats Dashboard**
Create a dashboard where users can keep track of the total number of applications submitted/rejected/waiting response/etc. and can set a goal for the number of submissions they want to make per month/week.
* **Calendar**
Create a page where the user can see all of their scheduled assessments, interviews and other upcoming deadlines. Integrate this functionality with Google Calendar.
* **Custom CV Sections**
The application is currently very opinionated about which sections to include in the CV (Education, Skills, Work History, ...) and in which order. Allow users to create custom sections and order them at will.
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
