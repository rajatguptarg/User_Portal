from my_app import db

class UserInfo(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    uname = db.Column(db.String(255), primary_key=True)
    pwd = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    role = db.Column(db.String(255))
    #price = db.Column(db.Float)

    def __init__(self, name, uname, pwd, gender, role):
        self.name = name
        self.uname = uname
        self.pwd = pwd
        self.gender = gender
        self.role = role

    #def __repr__(self):
    #    return '<Username %s>' % self.uname