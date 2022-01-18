from datetime import datetime
from distutils.log import debug
from email.policy import default
import re
from turtle import pos, title
from flask import Flask, redirect, url_for, request,render_template

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)



class Posts(db.Model):
    id = db.Column(db.Integer, primary_key =  True)
    title = db.Column(db.String(100),nullable = True)
    content = db.Column(db.Text,nullable = True)
    author = db.Column(db.String(20),nullable = True, default ="N/A")
    date_posted = db.Column(db.DateTime,nullable = True, default= datetime.utcnow)

    def __repr__(self):
        return "Blog Post " + str(self.id)

@app.route('/home')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addPost', methods=['GET','POST'])
def addPost():
   
    if request.method == 'POST':
        post = Posts(title = request.form['title'], author=request.form['author'], content=request.form['content'])
        db.session.add(post)
        db.session.commit()
        return render_template('posts.html')
    else:
        return render_template('add_post.html')

@app.route('/posts', methods=['GET','POST'])
def allPosts():
   
    if request.method == 'POST':
        post = Posts(title = request.form['title'], author=request.form['author'], content=request.form['content'])
        # to add seperatly
        #title = request.form.title
        # post = Posts(title = title, ...)
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')
    else:
        posts = Posts.query.order_by('date_posted').all()
        return render_template('posts.html',posts=posts)

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def editPost(id):
    post = Posts.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)

@app.route('/posts/delete/<int:id>')
def deletePost(id):
    db.session.delete(Posts.query.get(id))
    db.session.commit()
    return redirect('/posts')
if __name__ == "__main__":
    app.run(debug=True)