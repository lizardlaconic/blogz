from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key="hi"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    babblings = db.Column(db.String(1000))

    def __init__(self, title, babblings):
        self.title = title
        self.babblings = babblings

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods = ['GET'])
def blog():
    #form_value = request.args.get('param_name')
    single = request.args.get('id')
    if not single:
        tasks = Blog.query.all()

        return render_template('todos.html', tasks=tasks)

    else:
        #db.users.filter_by(name='Joe')
        tasks = Blog.query.filter_by(id=single).all()
        return render_template('single.html', tasks=tasks[0])

@app.route('/newpost', methods = ['POST' , 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        if title and blog:
            new_blog = Blog(title, blog)
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
            return render_template('newentry.html', title=title, blog=blog)

    tasks = Blog.query.all()

    return render_template('newentry.html', title='', blog='')

@app.route('/delete', methods=['POST'])
def delete():
    blog_id = int(request.form['task-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
