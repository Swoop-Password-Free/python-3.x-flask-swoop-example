from flask import Flask, request, redirect, session, render_template, url_for, flash
from requests_oauthlib import OAuth2Session
import jwt
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'Flask secret key'

# OAuth details
authorization_base_url = 'https://auth.swoop.email/oauth2/authorize'
token_url = 'https://auth.swoop.email/oauth2/token'

# Add your Swoop account details
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
callback_url = 'http://localhost:5000/auth/swoop/callback'

# Routes...

@app.before_request
def before_request():
    # secure the 'logged in' page

    if request.endpoint == 'logged_in' and 'email' not in session:
        flash('Please login!')
        return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logged_in', methods=['GET'])
def logged_in():
    email = "user"
    if session.get('email'):
        email = session['email']
    return render_template('logged_in.html', email=email)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET'])
def login():
    # Redirect the user to the Swoop OAuth server
    # using a URL with a the correct OAuth parameters.

    global authorization_base_url
    global client_id

    swoop = OAuth2Session(client_id)
    authorization_url, state = swoop.authorization_url(authorization_base_url)

    # build the authorization URL with the required query parameters
    authorization_url += '?response_type=code&redirect_uri=' + callback_url + '&scope=email'

    # state is used to prevent CSRF, keep for the callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/auth/swoop/callback')
def callback():
    # The user has been redirected back from Swoop to our callback URL.
    # With this redirection comes an authorization code included in the redirect URL.
    # We use that code to obtain an access token.

    try:
        state_from_request = request.args.get('state')
        code = request.args.get('code')
        swoop = OAuth2Session(client_id, state=session['oauth_state'],redirect_uri=callback_url)
        token = swoop.fetch_token(token_url, client_secret=client_secret, code=code, authorization_response=request.url)

        # get the user's email address from the web token
        payload = jwt.decode(token['id_token'], client_secret, audience=client_id, algorithms=["HS256"])
        email = payload['email']

        session.clear()
        session['email'] = email
        return redirect(url_for('logged_in'))

    except Exception as e:
        session.clear()
        return redirect(url_for('index'))
