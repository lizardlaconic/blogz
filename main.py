from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:asdf@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key="hi"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    babblings = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, babblings, owner):
        self.title = title
        self.babblings = babblings
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    elephant = db.relationship('Blog', backref='owner')
    #tasks = db.relationship('Task', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        #print("BBBBBBBBB\nBBBBBBBBB\nBBBBBBBBB\nBBBBBBBBB\nBBBBBBBBB\nBBBBBBBBB\n")
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    #print("CCCCCCCC\nCCCCCCCC\nCCCCCCCC\nCCCCCCCC\nCCCCCCCC\nCCCCCCCC\n")
    #if 'username' in session:
    #    flash("logged out")
    #    del session['username']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            #flash("Logged in")
            return redirect('/newpost')
        else:
            if user:
                flash("password incorrect")
            else:
                flash("username not in database")
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n")
    return render_template('login.html', password="", username="")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        flash("logged out")
        del session['username']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        formval = True

        if len(username) <3:
            flash("no man, username has to be at least 3 characters")
            formval = False
        
        if len(username) > 20:
            flash("no man, username is too long")
            formval = False

        if " " in username:
            flash("are you serious?  no spaces in username")
            formval = False

        if password != verify:
            flash("your passwords don't match.  try again")
            formval = False

        if len(password) <3:
            flash("no man, password has to be at least 3 characters")
            formval = False
        
        if len(password) > 20:
            flash("no man, password is too long")
            formval = False

        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash("No, man, that user already exists.")
            formval = False

        if formval:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/blog')

@app.route('/')
def index():
    #print("DDDDDDDDDDD\nDDDDDDDDDDD\nDDDDDDDDDDD\nDDDDDDDDDDD\nDDDDDDDDDDD\nDDDDDDDDDDD\n")
    #return redirect('/login')
    username=""
    if 'username' in session:
        username=session['username']
    guys = User.query.all()
    return render_template('index.html', users=guys, username=username)

@app.route('/blog', methods = ['GET'])
def blog():
    #print("aaaaaaa\naaaaaaa\naaaaaaa\naaaaaaa\n")
    username=""
    guy=""
    if 'username' in session:
        username=session['username']
    single = request.args.get('id')
    guy = request.args.get('guy')
    #print("aaaaaaa\naaaaaaa\naaaaaaa\naaaaaaa\n" + guy)
    #if 'username' in session and not single:
    #    owner = User.query.filter_by(username=session['username']).first()
    #    tasks = Blog.query.filter_by(owner=owner).all()

    #    return render_template('todos.html', tasks=tasks, username=session['username'])

    #elif single:
    if guy:
        owner = User.query.filter_by(id=guy).first()
        if owner:
            tasks = Blog.query.filter_by(owner=owner).all()
            guy=owner.username
            #tasks = Blog.query.filter_by(owner_id=1).all()
            return render_template('todos.html', tasks=tasks, username=username, guy=guy)
        else:
            flash("user not in database")
            return render_template('todos.html', tasks="", username=username, guy="")

    elif single:
        tasks = Blog.query.filter_by(id=single).all()
        if tasks:
            return render_template('single.html', tasks=tasks[0], username=username)
        else:
            flash("blog entry not in database")

    #else:
    tasks = Blog.query.all()
    return render_template('todos.html', tasks=tasks, username=username, guy=guy)

@app.route('/newpost', methods = ['POST' , 'GET'])
def newpost():
    #print("zzzzzzzzzzzz\nzzzzzzzzzzzz\n" + session['username'] +"\nzzzzzzzzzzzz\nzzzzzzzzzzzz\nzzzzzzzzzzzz\n")
    if request.method == 'POST':
        #print("gggggggggg\ngggggggggg\ngggggggggg\ngggggggggg\ngggggggggg\ngggggggggg\ngggggggggg\ngggggggggg\n")
        title = request.form['title']
        blog = request.form['blog']
        if title and blog:
            #print("aaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\naaaaaaaaaaaaa\n")
            owner = User.query.filter_by(username=session['username']).first()
            new_blog = Blog(title, blog, owner)
            db.session.add(new_blog)
            db.session.commit()
            #tasks = Blog.query.filter_by(id=single).all()
            #return render_template('single.html', tasks=tasks[0])
            ####
            db.session.flush()
            db.session.refresh(new_blog)
            return redirect('/blog?id='+str(new_blog.id))
            # #### 
        
            #tasks = Blog.query.all()
            #return render_template('todos.html',tasks=tasks)
        else:
            if not title:
                flash("Enter a depressing title")
            if not blog:
                flash("Enter a melodramatic blog post")
            return render_template('newentry.html', title=title, blog=blog, username=session['username'])

    #tasks = Blog.query.all()

    return render_template('newentry.html', title='', blog='', username=session['username'])

@app.route('/delete', methods=['POST'])
def delete():
    blog_id = int(request.form['task-id'])
    if 'username' in session:
        owner = User.query.filter_by(username=session['username']).first()
        blog = Blog.query.get(blog_id)
        
        if blog.owner_id == owner.id:
            db.session.delete(blog)
            db.session.commit()
        else:
            flash("you don't own that post, you can't delete it")

    return redirect(request.referrer)


if __name__ == '__main__':
    app.run()
