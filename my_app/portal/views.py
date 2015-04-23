from flask import request, jsonify, Blueprint, Flask, render_template,\
    redirect, url_for, session
from my_app.portal.models import UserInfo
from my_app import db


portal = Blueprint('portal', __name__)

@portal.route('/')
@portal.route('/index')
@portal.route('/home')
def home():
    """
    Render Home Page
    """
    return render_template('index.html')


@portal.route('/signin')
def signin():
    """
    Render Sign In Form
    """
    tag = 'sign_in'
    return render_template('signup.html', tag=tag)


@portal.route('/signup')
def signup():
    "Render Sign Up form"
    tag = 'sign_up'
    return render_template('signup.html', tag=tag)


@portal.route('/status', methods=['POST'])
def status():
    "Display status of current user"
    name = request.form.get('name')
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    gender = request.form.get('gender')
    role = request.form.get('role')
    user_info = UserInfo(name, uname, pwd, gender, role)
    db.session.add(user_info)
    db.session.commit()
    message = 'User registration successfully done.'
    return render_template('status.html', message=message)


@portal.route('/login_status', methods=['POST'])
def login():
    "Login user and Administrator to their accounts"
    uname_log = request.form.get('uname')
    pwd_log = request.form.get('pwd')
    try:
        user = UserInfo.query.filter_by(uname=uname_log).first()
        password = user.pwd
        role = user.role
        if password == pwd_log and role == 'Administrator':
            return redirect(url_for('portal.view_admin', user_name=uname_log))
        elif password == pwd_log and role != 'Administrator':
            return redirect(url_for('portal.view_admin', user_name=uname_log))
        else:
            message = 'Oops, We think you provided wrong Password. Try Again..!!'
    except Exception, e:
        message = 'Oops, We think you provided wrong Username. Try Again..!!'
    return render_template('status.html', message=message)



@portal.route('/user/<user_name>')
@portal.route('/admin/<user_name>')
def view_admin(user_name):
    "Home page for Administrator"
    user = UserInfo.query.filter_by(uname=user_name).first()
    res = {}
    name = user.name
    password = user.pwd
    role = user.role
    gender = user.gender
    data = {'user':user_name, 'name':name, 'password':password, 'role':role, 'gender':gender}
    all_users = UserInfo.query.all()
    for one_user in all_users:
        res[one_user.uname] = {
            'name': str(one_user.name),
            'password': str(one_user.pwd),
            'role': str(one_user.role),
            'gender':str(one_user.gender)
        }

    return render_template('admin.html', data=data, res=res, role=role)


@portal.route('/settings/<user_name>')
def user_settings(user_name):
    "Render the page to change the information of users"
    user = user_name
    details = user = UserInfo.query.filter_by(uname=user).first()
    name = details.name
    pwd = details.pwd
    role = details.role
    gender = details.gender
    data = {'name':name, 'password':pwd}
    return render_template('settings.html', user=user)


@portal.route('/update', methods=['POST'])
def update_data():
    "update the information of users into database"
    name_log = request.form.get('name')
    uname_log = request.form.get('uname')
    pwd_log = request.form.get('pwd')
    gender_log = request.form.get('gender')
    role_log = request.form.get('role')
    try:
        user = UserInfo.query.filter_by(uname=uname_log).first()
        user.name = name_log
        user.pwd = pwd_log
        user.gender = gender_log
        user.role = role_log
        db.session.commit()
        message = 'Your record has been updated in our database.'
    except Exception, e:
        message = 'We are facing some difficulties in updating your data. Check your username.'
    return render_template('status.html', message=message)
