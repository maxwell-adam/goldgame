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
    	</html>
    	"""

@app.route('/account/<username>')
def account(username):
    """Return the matching account resource"""
    account = {}
    account['name'] = username
    account['gold'] = 100
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
    """Return the matching business resource"""
    Physical_products = {}
    Physical_products['name'] = productname
    Physical_products['price'] = 0.5
    return str(Physical_products)
    
    
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
