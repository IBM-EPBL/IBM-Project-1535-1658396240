from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from markupsafe import escape
from flask import flask  


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=<HOSTNAME>;PORT=<PORT NUMBER>;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=<USERNAME>;PWD=<PASSWORD>",'','')
print(conn)
print("connection successful...")

app = Flask(__name__)
app.secret_key="123"

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/profile')
def profile():
   return render_template('profile.html')


@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/customerlogin',methods=["GET","POST"])
def customerlogin():
   if request.method=='POST':
      cemail=request.form['cemail']
      cpassword=request.form['cpassword']

      sql =f"select * from users where cemail='{escape(cemail)}' and cpassword='{escape(cpassword)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      data = ibm_db.fetch_both(stmt)

      if data:
         session["cemail"]=escape(cemail)
         session["cpassword"]=escape(cpassword)
         return redirect("profile")
      else:
         flash("Username and Password Mismatch","danger")
         return redirect(url_for("index"))
   return render_template('customerlogin.html')

@app.route('/customerregister',methods = ['POST', 'GET'])
def customerregister():
   if request.method == 'POST':
      try:
         cname = request.form['cname']
         cemail = request.form['cemail']
         cpassword = request.form['cpassword']
         cconfirmpassword = request.form['cconfirmpassword']

      
         insert_sql ="INSERT INTO users(cname,cemail,cpassword,cconfirmpassword)VALUES(?,?,?,?)"
         prep_stmt = ibm_db.prepare(conn,insert_sql)
         ibm_db.bind_param(prep_stmt,1,cname)
         ibm_db.bind_param(prep_stmt,2,cemail)
         ibm_db.bind_param(prep_stmt,3,cpassword)
         ibm_db.bind_param(prep_stmt,4,cconfirmpassword)
         ibm_db.execute(prep_stmt)
         flash("Register successfully","success")        
      except:
         flash("Error","danger")
      finally:
         return redirect(url_for("index"))
         con.close()
   return render_template('customerregister.html')



if __name__ == '__main__':
   app.run(debug = True)


