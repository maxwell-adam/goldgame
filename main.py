from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return """
    	<html>
    	<a href="/account/maxwell.adam">account</a>
    	<a href="/business/goodyear_tires">business</a>
    	<a href="/bankaccount/maxwell.adam">bankaccount</a>
    	</html>
    	"""

@app.route('/account/<username>')
def account(username):
    """Return the matching account resource"""
    account = {}
    account['name'] = username
    #account['gold'] = 100
    return str(account)

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
def Physical_products(productname):
    """Return the matching product resource"""
    Physical_products = {}
    Physical_products['name'] = productname
    Physical_products['price'] = 0.5
    return str(Physical_products)
    
@app.route('/bankaccount/<username>')
def bankaccount(username):
    """Return the matching business resource"""
    bankaccount= {}
    bankaccount['name'] = username + "\'s bank account"
    bankaccount['owner'] = username
    bankaccount['balance'] = 1
    return str(bankaccount)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, you stuffed this URL.', 404
