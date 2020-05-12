# JobTracker

JobTracker is a web application that helps users prepare customized job application materials and keep track of application statuses, deadlines, job descriptions and job details for all positions the user has applied for during their job search process.

![JobTracker](https://raw.githubusercontent.com/dtrifuno/)

## Built With

The backend is written in Python using the [Flask](https://flask.palletsprojects.com/) web microframework. It uses the [SQLAlchemy](https://www.sqlalchemy.org/) ORM and [Graphene](https://graphene-python.org/) to implement a GraphQL endpoint.

The frontend is a [Vue.js](https://vuejs.org/) application written in JavaScript, using [Vuex](https://vuex.vuejs.org/) for state management, [Apollo Link](https://www.apollographql.com/docs/link/) as a low-level GraphQL client and the [Bootstrap](https://getbootstrap.com/) CSS framework with the [Lux](https://bootswatch.com/lux/) color theme for styling.

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

### Compiles and hot-reloads for development

### Compiles and minifies for production

## TODO
* **Stats Dashboard**
Create a dashboard where users can keep track of the total number of applications in a given status, the number of applications submitted in a given month or week, etc.
* **Calendar**
Create a page where the user can see all of their scheduled assessments, interviews and other upcoming deadlines. Integrate this functionality with Google Calendar.
* **Testing**
Write unit and functional tests.
* **Containerize**
Package the application as a Docker container.

## License

[MIT](https://choosealicense.com/licenses/mit/)
