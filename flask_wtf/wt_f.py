from flask import Flask, request, render_template, redirect,url_for,session,flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
app=Flask(__name__)
app.secret_key="rjdk8741tao"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Deva'
app.config['MYSQL_PASSWORD'] = 'rjdk8741tao'
app.config['MYSQL_DB'] = 'emp'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("form.html")

class user:
    def __init__(self,id,username, password):
        self.id=id
        self.username=username
        self.password=password

class signup(FlaskForm):
    username=StringField("username",validators=[InputRequired(),Length(min=4,max=15)])
    password=PasswordField("password",validators=[InputRequired(),Length(min=8,max=15)])
    submit=SubmitField("Signup")
class LoginForm(FlaskForm):
    username=StringField("username",validators=[InputRequired(),Length(min=4,max=15)])
    password=PasswordField("password",validators=[InputRequired(),Length(min=8,max=15)])
    submit=SubmitField("Login")

@app.route("/signin",methods=["GET","POST"])
def signin():
    form=signup()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        cur=mysql.connection.cursor()
        cur.execute("Select id from data1 where name=%s",(username,))
        old_user=cur.fetchone()
        if old_user:
            cur.close()
            flash("Username already taken, Please try different one.","danger")
            return render_template("signin.html",form=form)
        cur.execute("insert into data1 (name,password) values (%s, %s)",(username,password))
        mysql.connection.commit()
        cur.close()
        flash('Signup successful','success')
        return redirect(url_for("login"))
    return render_template("signin.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        cur=mysql.connection.cursor()
        cur.execute("select id ,name, password from data1 where name=%s",(username,))
        userdata=cur.fetchone()
        cur.close()
        if userdata and userdata[2]==password:
            currentuser=user(id=userdata[0],username=userdata[1],password=userdata[2])
            session["user_id"]=currentuser.id
            flash("Login Successful","Success")
            return redirect(url_for("home"))
        else:
            flash("Invalid Credentials","Danger")
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    session.pop("user_id",None)
    flash("Logged Out","Success")
    return redirect(url_for("home"))
if __name__=="__main__":
    app.run(debug=True)