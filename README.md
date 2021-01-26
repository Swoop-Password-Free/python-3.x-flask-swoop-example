This example demonstrates how to use [Python](https://python.org/) 3.x and
[Flask](https://palletsprojects.com/p/flask/) to authenticate users using [Swoop](https://swoopnow.com).  Use
this example as a starting point for your own web applications.

## Instructions

To install this example on your computer, clone the repository and install
dependencies.

```bash
$ git clone git@github.com:Swoop-Password-Free/python-3.x-flask-swoop-example.git
$ cd python-3.x-flask-swoop-example
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install Flask requests requests_oauthlib cryptography pyjwt
```

The example uses variables `index.py` to configure the client id and client
secret needed to access the Swoop API.  Update those variables with your Swoop
Property credentials obtained from [Swoop](https://dashboard.swoop.email).

Make sure to set the `redirect URL` for the property to `http://localhost:5000/auth/swoop/callback`

```bash
export FLASK_APP=index.py
flask run
```

Open a web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
to see the example in action.
