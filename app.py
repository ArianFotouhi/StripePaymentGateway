from flask import Flask, render_template, request
import stripe
import configparser

config = configparser.ConfigParser()
config.read('setting.ini')


# Access values from the INI file
secret_key = config['KEYS']['SECRET_KEY']
publish_key = config['KEYS']['PUBLISH_KEY']


stripe_keys = {
  'secret_key': secret_key,
  'publishable_key': publish_key
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    #in cents
    amount = 50

    customer = stripe.Customer.create(
        email='',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='cad',
        description='payment'
    )

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)