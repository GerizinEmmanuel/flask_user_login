from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    telefone = db.Column(db.String(15))
    auth2 = db.Column(db.Boolean)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    @property
    def is_annonimous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    def __init__(self, username, password, name, email, telefone):
        self.username=username
        self.password=password
        self.name=name
        self.email=email
        self.telefone=telefone
    
    def __init__(self, username, name, email, telefone):
        self.username=username
        self.name=name
        self.email=email
        self.telefone=telefone
        
    def __repr__(self):
        return '<User %r>' % self.username        


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id=user_id
    
    def __repr__(self):
        return '<Post %r>' % self.id
    

class Follow(db.Model):
    __tablename__ = "follow"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    user = db.relationship('User',foreign_keys=[user_id])
    follower = db.relationship('User',foreign_keys=[follower_id])

    def __init__(self,user_id,follower_id):
        self.user_id=user_id
        self.follower_id=follower_id

        
