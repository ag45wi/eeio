from flask import Flask, render_template, Response, request, redirect, url_for, session
import matplotlib.pyplot as plt
import io
import base64
import os
import pandas as pd
import numpy as np
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

from util_app import get_lst_agg, generate_chart_agg, delete_files_in_directory, get_df_input
from util_mat import calc_mat
from db_config import db_init, get_hash_password

app = Flask(__name__)
mysql = db_init(app)

@app.route('/')
def home():
   lst=get_lst_agg()
   #return "Hello EEIO2"
   return render_template("nav_display.html", data_list=lst, selected_opt_agg="--All_Sectors--")
   #return render_template("navbar.html", data_list=lst, selected_opt_agg="Energy")


@app.route('/submit_opt_agg', methods=['POST'])
def submit_opt_agg():
   lst=get_lst_agg()
   selected_option = request.form['dropdown']
   return render_template("nav_display.html", data_list=lst, selected_opt_agg=selected_option)

@app.route('/plot_png/<in_agg>')
def plot_png(in_agg):
   #https://plotly.com/python/creating-and-updating-figures/
   #pip install kaleido
   print("inside /plot_png")
   img=generate_chart_agg(in_agg).to_image(format="png")
   return Response(img, mimetype='image/png')

##Upload files-----------------------------------------------

# Set the upload folder
#https://stackoverflow.com/questions/51733419/flask-file-upload-is-not-saving-the-file
#https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/

#cwd="/home/inovasi9/app_eeio"
cwd=os.getcwd()
#UPLOAD_FOLDER = './static/uploads'
UPLOAD_FOLDER = cwd+'/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/nav_matrix')
def nav_matrix():
   empty_arr=np.asarray([])
   return render_template("nav_matrix.html", labeled_files=empty_arr, df_tables=empty_arr)

@app.route('/upload', methods=['POST'])
def upload():

    delete_files_in_directory(app.config['UPLOAD_FOLDER'])

    #if 'files' not in request.files:
    #    return 'No file part'
    
    file_io = request.files['f_io']
    file_fec = request.files['f_fec']
    file_conv = request.files['f_conv']
    file_co2 = request.files['f_co2']

    file_arr = [file_io, file_fec, file_conv, file_co2]
    #files = request.files.getlist("files") 
    #print ("len(files)", len(files))

    uploaded_files = []
    label_files = ['f_io', 'f_fec', 'f_conv', 'f_co2']
    #for file in files:
    for file in file_arr:
      #if file.filename == '':
      #   return 'No selected file'
      #print (f'file.filename {file.filename}')

      uploaded_files.append(file.filename)

      if file and allowed_file(file.filename):
         filename = file.filename
         #print (f'Filename {filename}')
         file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
         #print("file_path", file_path)
         file.save(file_path)
         #print (f'File {file_path} uploaded successfully')

         #uploaded_files.append(filename)

         #return f'Files uploaded successfully: {", ".join(uploaded_files)}'
         #return redirect(url_for('show_content2', uploaded_files=uploaded_files))
    
    #df_uploaded_files=pd.DataFrame(data=uploaded_files, index=['f_io', 'f_fec', 'f_conv', 'f_co2'])
    label_vert=np.array(label_files).reshape(-1,1)
    file_vert=np.array(uploaded_files).reshape(-1,1)
    labeled_files=np.hstack((label_vert, file_vert))
    #print("labeled_files", labeled_files)

    empty_arr=np.asarray([])
    return render_template("nav_matrix.html",labeled_files=labeled_files, df_tables=empty_arr)
    #return 'File not allowed'

@app.route('/calc_matrix', methods=['POST'])
def calc_matrix():
   print("inside calc_matrix")
   fname_io = request.form['f_io']
   fname_fec = request.form['f_fec']
   fname_conv = request.form['f_conv']
   fname_co2 = request.form['f_co2']

   #print("calc_matrix::labeled_files", file_io)

   df_agg_sectors, df_agg_sectors_each=calc_mat(fname_io, fname_fec, fname_conv, fname_co2)
   #return "ret calc_matrix::labeled_files"
   df_agg_sectors.reset_index(inplace=True)
   print("df_agg_sectors", df_agg_sectors.head(5))

   empty_arr=np.asarray([])
   #https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
   return render_template("nav_matrix.html",labeled_files=empty_arr, df_tables=[df_agg_sectors.to_html(classes='data', header="true")])

#Menu display input data-------------------------------------------------
@app.route('/nav_input')
def nav_input():
   df_io, df_fec, df_conv, df_co2=get_df_input()

   return render_template("nav_input.html",df_io=[df_io.to_html(classes='data', header="true")], df_fec=[df_fec.to_html(classes='data', header="true")], df_conv=[df_conv.to_html(classes='data', header="true")], df_co2=[df_co2.to_html(classes='data', header="true")])
   

# DB----------------------------------------------------------------------------

@app.route('/login')
def login():
    return redirect(url_for('nav_login', mode='prompt'))
    
@app.route('/nav_login/<mode>', methods=['GET', 'POST'])
def nav_login(mode):
   #return f"Hello nav_login {mode}"
   if (mode == "prompt"):
      message = ''
      if request.method == 'POST' and 'userid' in request.form and 'password' in request.form:
         
         userid = request.form['userid']
         password = get_hash_password(request.form['password'])
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('SELECT * FROM user WHERE userid = % s AND password = % s', (userid, password, ))
         user = cursor.fetchone()
         if user:
               print(f"login ok {userid}")
               session['loggedin'] = True
               session['userid'] = user['userid']
               session['name'] = user['name']
               session['email'] = user['email']
               message = 'Logged in successfully !'
               return redirect(url_for('home'))
         else:
               print(f"login NOT ok {userid}")
               message = 'Please enter correct email / password !'
      #return f"Hello2 nav_login {mode}"
      return render_template('nav_login.html', message=message, mode=mode)

   elif (mode=="register"):
      message = ''
      if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
         userID = request.form['userid']
         userName = request.form['name']
         password = get_hash_password(request.form['password'])
         email = request.form['email']
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
         account = cursor.fetchone()
         if account:
               message = 'Account already exists !'
         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
               message = 'Invalid email address !'
         elif not userName or not password or not email:
               message = 'Please fill out the form !'
         else:
               cursor.execute(
                  'INSERT INTO user (userid, name, email, password) VALUES (% s, % s, % s, % s)', (userID, userName, email, password, ))
               mysql.connection.commit()
               message = 'You have successfully registered !'
      elif request.method == 'POST':
         #print("fill in request form")
         message = 'Please fill out the form !'
      
      return render_template('nav_login.html', message=message, mode=mode)

   elif (mode=="logout"):
      session.pop('loggedin', None)
      session.pop('userid', None)
      session.pop('email', None)
      return redirect(url_for('nav_login', mode='prompt'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('nav_login', mode='prompt'))


if __name__ == '__main__':
   app.run(debug=True)