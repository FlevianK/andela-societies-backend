[![Codacy Badge](https://api.codacy.com/project/badge/Grade/afbc8438e34a48fea86d20a953bf6998)](https://app.codacy.com/app/jonathankamau/andela-societies-backend?utm_source=github.com&utm_medium=referral&utm_content=AndelaOSP/andela-societies-backend&utm_campaign=badger)
[![CircleCI](https://circleci.com/gh/AndelaOSP/andela-societies-backend.svg?style=svg)](https://circleci.com/gh/AndelaOSP/andela-societies-backend)
[![Coverage Status](https://coveralls.io/repos/github/AndelaOSP/andela-societies-backend/badge.svg?branch=setup-circle-ci)](https://coveralls.io/github/AndelaOSP/andela-societies-backend?branch=setup-circle-ci)

# Society-platform ✍
API for an Andela Societies.

```Insert Description here```

- ## API
This App exposes endpoints that allows ```clients/Users``` to interact with Andela society Platform.

- #### Available Resource Endpoints

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v1.0/login` | Login user.|


## Getting Started 🕵
- To run on local machine git clone this project :
```
 $ git clone https://github.com/AndelaOSP/andela-societies-backend.git
 ```

 Copy and paste the above command in your terminal, the project will be downloaded to your local machine.

- To consume API in client of choice navigate to:
 ```
 <Insert Hosted site here>
 ```

### Prerequisites
The application is built using python: flask framework.
>[Flask](http://flask.pocoo.org/) is a microframework for the Python programming language.


To Install python checkout:
```
https://www.python.org/
```


### Installing
For this section I will assume you have python3 and it's configured on your machine. </br>
Navigate to the folder you cloned and run: </br>

- Install Requirements
```
$ cd src
$ pip install -r requirements.txt
```

- Configure Environment.
```
<Insert Config here>
```
> Note replace the value for DEV_DATABASE with real database path and SECRET with a strong string value


- Configure database
```
<Insert Config here>
```

- Run App 🏃
```
$ cd src
$ python manage.py runserver
```
The app should be accessiable via : http://127.0.0.1:5000/



## Running the tests

```
$ cd src
$ python manage.py test
```

- Coding style tests

[Pep8](https://www.python.org/dev/peps/pep-0008/) standards are followed in project.

```
$ cd src
$ pep8 api --count

```

## Deployment 🚀

- [Check this out to deploy to heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)

## Built With  🏗 🔨⚒

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flaskrestplus](https://flask-restplus.readthedocs.io/en/stable/) - Extension for Flask that adds support for quickly building REST APIs.

## Contributing 👍

- Please Fork me! :-)

## Versioning ⚙

- [Checkout our releases](https://github.com/AndelaOSP/andela-societies-backend/releases)

## Authors 📚

* **AndelaOSP**


## License 🤝

- This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments 🙏

* [Andela ](https://andela.com/) - We are hiring !
* [Motivation](https://www.youtube.com/watch?v=dQw4w9WgXcQ) - BEST RESOURCE EVER!!! 🤓🤓
