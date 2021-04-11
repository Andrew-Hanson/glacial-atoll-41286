import os
import base64
import copy

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        name = copy.copy(request.form['name'])
        amount = copy.copy(int(request.form['amount']))
        donor = Donor(name=name)
        flag = False
        for selected_donor in list(Donor.select()):
            if selected_donor.name != name:
                pass
            else:
                donor = selected_donor
                flag = True
                break
        if not flag:
            donor.save()
        donation = Donation(value=amount, donor=donor)
        donation.save()

        return all()
    else:
        return render_template('add_donations.jinja2')
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

