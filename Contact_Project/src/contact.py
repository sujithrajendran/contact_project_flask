from flask.app import Flask
from flask.globals import request
from flask.templating import render_template 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='oracle://system:akshaya@localhost:1521/XE'
db=SQLAlchemy(app)
class contact(db.Model):
    __tablename__ = 'contact_detail'
    name =db.Column(db.String(25))
    mobile_no=db.Column(db.Integer,primary_key=True)
    s_no=db.Column(db.Integer)
    email_id=db.Column(db.String(30))
    gender=db.Column(db.String(10))
@app.route('/')
@app.route('/homepage',methods=['GET','POST'])
def contact_info():
    return render_template('home.html')
@app.route('/addpage',methods=['GET','POST'])
def add():
    if request.method=='GET':
        return render_template('add.html')
    elif request.method=='POST':
        name=request.form['Name']
        number=request.form['Number']
        snumber=request.form['SNumber']
        emailid=request.form['Email']
        gender=request.form['Gender']
        if len(str(number))==10 and len(str(number))==10:
            conn=contact(name=name.upper(),mobile_no=number,s_no=snumber,email_id=emailid,gender=gender)
            db.session.add(conn)
            db.session.commit()
            return render_template('home.html')
        else:
            return render_template("alert.html")
@app.route('/updatepage',methods=['GET','POST'])
def update():
    if request.method=='GET':
        return render_template('update.html')
    elif request.method=='POST':
        name=request.form['Name']
        number=request.form['Number']
        snumber=request.form['SNumber']
        emailid=request.form['Email']
        if len(str(number))==10 and len(str(number))==10:
            conn=contact.query.filter(contact.name==name.upper()).one()
            conn.mobile_no=number
            conn.s_no=snumber
            conn.email_id=emailid
            db.session.add(conn)
            db.session.commit()
            return render_template('home.html')
        else:
            return render_template("alert.html")
@app.route('/searchpage',methods=['GET','POST'])
def search():
    if request.method=='GET':
        return render_template('search.html')
    elif request.method=='POST':
        name=request.form['Search']
        conn=contact.query.filter(contact.name.like(name.upper()+'%')).all()
        return render_template('show.html',cont=conn)
@app.route('/deletepage',methods=['GET','POST'])
def delete():
    if request.method=='GET':
        return render_template('delete.html')
    elif request.method=='POST':
        name=request.form['Name']
        conn=contact.query.filter(contact.name==name.upper()).one()
        db.session.delete(conn)
        db.session.commit()
        return render_template('home.html')
if __name__=="__main__":
    db.create_all()
    app.run(debug=True,port=8071)