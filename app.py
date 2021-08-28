from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
UPLOAD_FOLDER='static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
db=SQLAlchemy(app)


class Post (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    details=db.Column(db.String(50))


class News(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    news_img=db.Column(db.String(50))
    news_heading=db.Column(db.String(50))
    news_date=db.Column(db.String(50))

db.create_all()

@app.route('/')
def admin_index():
    news=News.query.all()
    return render_template('index.html',news =news)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/show')
def show():
    posts=Post.query.all()
    return render_template('show.html',posts=posts)


@app.route('/create', methods=['GET','POST']) 
def create():
    
    if request.method=='POST':
        file=request.files['news_img']
        filename=file.filename
        file.save(os.path.join (app.config['UPLOAD_FOLDER'],filename))
        new=News(
        news_img=filename,
        news_heading=request.form['news_heading'],
        news_date=request.form['news_date']
        )
        db.session.add(new)
        db.session.commit()
        return redirect("/")
    return render_template('create_post.html')




@app.route('/post') 
def post(): 
    return render_template('post.html')

@app.route('/post', methods=['GET','POST']) 
def postadd():
    if request.method=='POST':
        post=Post(details=request.form.get('post'))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin_index'))

    return render_template('show.html')



if __name__ == '__main__':
    app.run(debug=True)