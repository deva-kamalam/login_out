from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
app=Flask(__name__)
app.secret_key="rjdk8741tao"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Deva'
app.config['MYSQL_PASSWORD'] = 'rjdk8741tao'
app.config['MYSQL_DB'] = 'log'
mysql = MySQL(app)
@app.route('/',methods=["GET","POST"])
def signup():
    if request.method=='POST':
        name=request.form.get("name")
        password=request.form.get("password")
        cur=mysql.connection.cursor()
        cur.execute("insert into signup (name,password) values (%s,%s)",(name,password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('signin'))
    return render_template("signup.html")
@app.route('/signin/',methods=["GET","POST"])
def signin():
    if request.method=='POST':
        session['name'] = request.form.get("name")
        name=session.get('name')
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("select * from signup where name=%s and password =%s",(name,password))
        data=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if data:
            session['name']=name
            return redirect(url_for('display'))
        else:
            return ('Invalid username or password', 'error')
    return render_template('signin.html')
@app.route('/display/',methods=["GET","POST"])
def display():
    cur = mysql.connection.cursor()
    cur.execute("select * from display" )
    data=cur.fetchall()
    cur.close()
    return render_template('display.html',display=data)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")

        cur = mysql.connection.cursor()
        cur.execute("UPDATE display SET name = %s, age = %s, email = %s WHERE id = %s", (name, age, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('display'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM display WHERE id = %s", (id,))
        data = cur.fetchone()
        cur.close()
        return render_template('edit.html', data=data)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM display WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Record deleted successfully', 'success')
    return redirect(url_for('display'))
if __name__ == '__main__':
    app.run(debug=True)
