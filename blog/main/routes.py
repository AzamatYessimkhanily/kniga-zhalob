from flask import Blueprint, render_template, url_for, request,redirect
from flask_login import current_user, login_required
from blog import db
from blog.models import Post2, Incident

main = Blueprint('main', __name__)



@main.route('/post/new', methods=['POST'])
def form():
    location = request.form['incident-location']
    description = request.form['incident-description']
    phone_number = request.form['phone-number']
    full_name = request.form['full-name']
    email = request.form['email']
    is_foundation_employee = request.form['is_foundation_employee']

    form_data = Incident(location=location, description=description, phone_number=phone_number, full_name=full_name, email=email, is_foundation_employee=is_foundation_employee)

    db.session.add(form_data)
    db.session.commit()

    return redirect(url_for('admin.index'))


@main.route('/')
def home():
   return render_template('index.html', title = 'UMC')

@main.route('/incidents')
def incidents():
    incidents = Incident.query.all()
    return render_template('incidents.html', incidents=incidents)



@main.route('/zae')
def zae():
    return render_template('zae.html', title = 'zae')
