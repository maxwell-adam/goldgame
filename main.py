import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from flask import *
app = Flask(__name__)

app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# INFORMATION MODEL ELEMENTS
# This is where we create all the information models to use in the application

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def account_key(account_name):
    """Constructs a Datastore key for a Account entity.

    We use account_name as the key.
    """
    return ndb.Key('Account', account_name)


class BankAccount(ndb.Model):
    """Sub model for representing a bank account."""
    name = ndb.StringProperty(indexed=False)
    balance = ndb.StringProperty(indexed=False)

class Account(ndb.Model):
    """A main model for representing an individual Account entry."""
    owner = ndb.StringProperty(indexed=True)
    usage = ndb.IntegerProperty(indexed=False, default=0)
    bankaccount = ndb.StructuredProperty(BankAccount)
    #content = ndb.StringProperty(indexed=False)
    #date = ndb.DateTimeProperty(auto_now_add=True)

def check_login():
    # FAKE this for now
    #user = users.get_current_user()
    user = "maxwell.adam@me.com"
    return user

def not_authorized():
    return 'Sorry, not authorized. Please login first', 403


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    user = check_login()
    return render_template('hello.html', name=user)


@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):

    # find out who has logged in with their Google Account
    user = check_login()

    if user is None:
        return not_authorized()
        
    if request.method == 'POST':
        """Create a matching account resource"""
        account = create_account(username)
    else:
        """Return the matching account resource"""

        # TODO: something about ancestor queries for consistency
        account_query = Account.query(Account.owner == username)
        accounts = account_query.fetch(1)

        # so we should have a collection of accounts with just *one* account in it
        try:
            account = accounts[0]
            account.usage += 1
            account.put()
            
        except:
            print "Couldn't find account. Creating"
            account = create_account(username)
            
    return str(account.to_dict())
    
def create_account(username):
    account = Account()
    account.owner = username
    account.player.name = username
    account.bankaccount = BankAccount()
    # and save it for the future!
    key = account.put()
    return account


@app.route('/bankaccount/<username>')
def bankaccount(username):
    """Return the matching business resource"""
    # find out who has logged in with their Google Account
    user = check_login()

    if user is None:
        return 'Sorry, not authorized. Please login first', 403

    bankaccount= {}
    bankaccount['name'] = username + "\'s bank account"
    bankaccount['owner'] = username
    bankaccount['balance'] = 1
    return str(bankaccount)

@app.route('/business/<businessname>')
def business(businessname):
    """Return the matching business resource"""
    business = {}
    business['name'] = businessname
    business['price'] = 50
    business['location'] = 'croydon'
    business['owner'] = 'maxwell.adam'
    return str(business)
    
@app.route('/product/<productname>')
def physical_products(productname):
    """Return the matching product resource"""
    physical_products = {}
    physical_products['name'] = productname
    physical_products['price'] = 0.5
    return str(physical_products)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, you stuffed this URL.', 404
