from flask import request, jsonify, Blueprint, Flask, render_template, redirect, url_for, session
from my_app.portal.models import UserInfo
from my_app import db


portal = Blueprint('portal', __name__)

@portal.route('/')
@portal.route('/index')
@portal.route('/home')
def home():
    return render_template('index.html')


@portal.route('/signin')
def signin():
    return render_template('signin.html')


@portal.route('/signup')
def signup():
    return render_template('signup.html')


@portal.route('/status', methods=['POST'])
def status():
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
    uname_log = request.form.get('uname')
    pwd_log = request.form.get('pwd')
    try:
        user = UserInfo.query.filter_by(uname=uname_log).first()
        password = user.pwd
        role = user.role
        if password == pwd_log and role == 'Administrator':
            return redirect(url_for('portal.view_admin', user_name=uname_log))
        elif password == pwd_log and role != 'Administrator':
            return redirect(url_for('portal.view_user', user_name=uname_log))
        else:
            message = 'Oops, We think you provided wrong Password. Try Again..!!'
    except Exception, e:
        message = 'Oops, We think you provided wrong Username. Try Again..!!'
    return render_template('status.html', message=message)


@portal.route('/admin/<user_name>')
def view_admin(user_name):
    user = UserInfo.query.filter_by(uname=user_name).first()
    res = {}
    #name = res[user_name]['name']
    #print nam
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

    return render_template('admin.html', data=data, res=res)
    #return redirect(url_for('portal.user_settings', data=data))
    #return jsonify(res)


@portal.route('/user/<user_name>')
def view_user(user_name):
    user = UserInfo.query.filter_by(uname=user_name).first()
    #res = {}
    '''
    for user in users:
        res[user.uname] = {
            'name': user.name,
            'password': str(user.pwd),
            'role': str(user.role),
            'gender':str(user.gender)
    }
    '''
    #name = res[user_name]['name']
    #print nam
    name = user.name
    password = user.pwd
    role = user.role
    gender = user.gender
    data = {'user':user_name, 'name':name, 'password':password, 'role':role, 'gender':gender}
    return render_template('user.html', data=data)

@portal.route('/settings/<user_name>')
def user_settings(user_name):
    user = user_name
    return render_template('settings.html', user=user)


@portal.route('/update', methods=['POST'])
def update_data():
    name_log = request.form.get('name')
    uname_log = request.form.get('uname')
    pwd_log = request.form.get('pwd')
    gender_log = request.form.get('gender')
    role_log = request.form.get('role')
    #user = UserInfo.query.filter_by(uname)
    #admin = User.query.filter_by(username='admin').first()
    #admin.email = 'my_new_email@example.com'

    try:
        user = UserInfo.query.filter_by(uname=uname_log).first()
        #admin = User.query.filter_by(username='admin').first()
        #admin.email = 'my_new_email@example.com'
        print user
        user.name = name_log
        user.pwd = pwd_log
        user.gender = gender_log
        user.role = role_log
        db.session.commit()
        message = 'Your record has been updated in our database.'
    except Exception, e:
        message = 'We are facing some difficulties in updating your data. Check your username.'
        #message = e
    return render_template('status.html', message=message)