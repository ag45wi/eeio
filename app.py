from flask import Flask, render_template, Response, request, redirect, url_for, session, send_file, jsonify, send_from_directory, abort
from flask_mail import Mail, Message
import matplotlib.pyplot as plt
import io
import base64
import os
import pandas as pd
import numpy as np
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from dotenv import load_dotenv
import sys

from util_app import get_year, get_dct_agg, get_dct_sector, get_dct_sectorByAgg,  generate_multichart, generate_multichart_years, delete_files_in_directory, format_df, get_df_input, save_file, clean_list_items, generate_csv
from util_mat import calc_mat
from util_db import db_init, get_hash_password, login_prompt, login_register, login_changePassword, get_table_user, verify_user, verify_email_byToken, delete_user

app = Flask(__name__)

load_dotenv()
db = db_init(app)

app.secret_key = os.environ["APP_KEY"]

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]
app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"]  # Use an app-specific password
mail = Mail(app)

DOWNLOAD_FOLDER = os.path.join(app.root_path, 'static', 'buf', 'download') 
#os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

#YEAR_LST=[] #get_year(db) #[2016]
YEAR=0 #YEAR_LST[0]
EEIO_FILES = ["IO", "FinalEnergyConsumption", "ConversionFactor", "DirectCO2EmmisionFactor"]

@app.route('/', methods=['GET', 'POST'])
def nav_home(): # This is the function name to pass to url_for()
   global YEAR
   print("inside nav_home")

   year_lst=get_year(db)
   #print("year_lst", year_lst)
   dct_year = {
      str(year): [year] for year in year_lst
   }
   dct_year['ALL'] = year_lst.copy()
   print("dct_year", dct_year)
   YEAR=list(dct_year.items())[0]

   dct_sector=get_dct_sector(db) #code: name
   dct_agg=get_dct_agg(db) #code: name
   dct_sector_byAgg=get_dct_sectorByAgg(db) #code_agg: list of sector codes
   #print("dct_sector_byAgg-0", len(dct_sector_byAgg), list(dct_sector_byAgg.items())[:5])

   dct_agg["ALL"]="ALL"
   #all_values = sorted({code for codes in dct_sector_byAgg.values() for code in codes})
   all_values=list(dct_sector.keys())
   print("all_values", len(all_values), all_values)

   dct_sector_byAgg['ALL'] = all_values
   print("dct_agg", dct_agg)
   print("dct_sector", dct_sector)
   print("dct_sector_byAgg", dct_sector_byAgg)

   return render_template("nav_display.html", dct_sector=dct_sector, dct_year=dct_year, dct_sector_aggregates=dct_sector_byAgg, dct_agg=dct_agg)


@app.route('/get_chart_data/<in_sector_str>/<in_year_str>')
def get_chart_data(in_sector_str, in_year_str):
   #https://plotly.com/python/creating-and-updating-figures/
   #pip install kaleido
   print(f"inside get_chart_data:: {in_sector_str}, {type(in_sector_str)}, {in_year_str}")

   sector_lst=in_sector_str.split(",")
   year_lst=in_year_str.split(",")
   year_lst=[int(y) for y in year_lst]
   #print("sector_lst", sector_lst)

   #chart_json_content = generate_multichart(db, sector_lst, year=int(in_year))
   chart_json_content = generate_multichart_years(db, sector_lst, years=year_lst)

   return Response(chart_json_content, mimetype='application/json')


@app.route('/download_data', methods=['POST'])
def download_data_route():
   """
   API endpoint to generate and serve a CSV file for download, using a POST request
   to avoid long URLs.
   """
   print("inside /download_data") 

   # Get the JSON data from the request body
   data = request.json
   if (not data) or ('sectors' not in data) or ('years' not in data) or ('dataType' not in data):
      print("Invalid request data")
      return jsonify({"error": "Invalid request data"}), 400

   sectors = data['sectors']
   years = data['years']
   report_type = data['dataType']

   print("sectors", sectors)
   print("years", years)
   print("report_type", report_type)
   
   try:
      fname_dl = generate_csv(db, sectors, years, report_type=report_type, dl_folder=DOWNLOAD_FOLDER)
      # Construct the URL for the client to download from
      # You'll need a new Flask route to serve these temporary files
      download_url = f"/get_download/{fname_dl}"
      return {"download_url": download_url}, 200 # Return JSON with the URL
   except Exception as e:
      print(f"Error generating CSV: {e}")
      return {"error": "Failed to generate CSV for download."}, 500   

@app.route('/get_download/<filename>', methods=['GET'])
def serve_generated_csv(filename):
   #https://gemini.google.com/app/ca042a5fefa69b8d
   # Basic security: Prevent directory traversal attacks
   # Ensure the filename is safe and within the allowed directory
   print("inside /get_download/ ->serve_generated_csv")
   print("os.path.basename(filename), filename", os.path.basename(filename), filename)

   if not os.path.basename(filename) == filename:
      abort(404) # Or 403, depending on your security preference

   try:
      # Flask's send_from_directory is secure and recommended
      response = send_from_directory(
         DOWNLOAD_FOLDER,
         filename,
         as_attachment=True,
         download_name=filename, # You can set a more user-friendly name if desired
         mimetype='text/csv'
      )
      return response
   except FileNotFoundError:
      abort(404) # File not found if it was cleaned up already or never created
   except Exception as e:
      print(f"Error serving file {filename}: {e}")
      import traceback
      traceback.print_exc()
      abort(500)

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

@app.route('/nav_matrix', methods=['GET', 'POST'])
def nav_matrix():

   msg_lst=[]
   if request.method == 'POST' and 'calc_matrix' in request.form:
      #delete_files_in_directory(app.config['UPLOAD_FOLDER'])

      file_io = request.files['f_io']
      file_fec = request.files['f_fec']
      file_conv = request.files['f_conv']
      file_co2 = request.files['f_co2']
      
      found=True
      if (not file_io and not file_fec and not file_conv and not file_co2):
         msg_lst=["Please upload one of the input files"]
         found=False
         #print("got here1")
      else:
         #print("got here2")
         if (file_io):
            rv, msg1=save_file(file_io, f"{EEIO_FILES[0]}.csv", YEAR)
            msg_lst.append(msg1)
         if (file_fec):
            rv, msg1=save_file(file_fec, f"{EEIO_FILES[1]}.csv", YEAR)
            msg_lst.append(msg1)
         if (file_conv):
            rv, msg1=save_file(file_conv, f"{EEIO_FILES[2]}.csv", YEAR)
            msg_lst.append(msg1)
         if (file_co2):
            rv, msg1=save_file(file_co2, f"{EEIO_FILES[3]}.csv", YEAR)
            msg_lst.append(msg1)

      if (found):
         #df_agg_sectors, df_agg_sectors_each=calc_mat(fname_io, fname_fec, fname_conv, fname_co2, YEAR)
         rv, msg1, df_agg_sectors, df_agg_sectors_each=calc_mat(EEIO_FILES, YEAR)
         msg_lst.append(msg1)

         if (rv):
            df_agg_sectors.reset_index(inplace=True)
            print("df_agg_sectors", df_agg_sectors.head(5))

            df_fmt=format_df(df_agg_sectors)
            html_tbl=df_fmt.to_html(classes='data', header="true")
         else:
            html_tbl=""
         #https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
         #return render_template("nav_matrix.html", df_tables=[df_agg_sectors.to_html(classes='data', header="true")])
         return render_template("nav_matrix.html", msg_lst=msg_lst, html_tbl=html_tbl)

   return render_template("nav_matrix.html", msg_lst=msg_lst)


#Menu display input data-------------------------------------------------
@app.route('/nav_viewData')
def nav_viewData():
   df_io, df_fec, df_conv, df_co2=get_df_input(EEIO_FILES, YEAR)

   html_io=df_io.to_html(classes='data', header="true")
   html_fec=df_fec.to_html(classes='data', header="true")
   html_conv=df_conv.to_html(classes='data', header="true")
   html_co2=df_co2.to_html(classes='data', header="true")

   return render_template("nav_viewData.html",html_io=html_io, html_fec=html_fec, html_conv=html_conv, html_co2=html_co2)


@app.route('/nav_inputCategory', methods=['GET', 'POST'])
def nav_inputCategory():
   if request.method == 'POST' and 'submit' in request.form:
      file_cat_lst = request.files['f_cat_lst']
      file_cat_det = request.files['f_cat_det']

      msg_lst=[]
      if (not file_cat_lst and not file_cat_det):
         msg_lst=["Please upload at least one of the category input files"]
      if (file_cat_lst):
         rv, msg1=save_file(file_cat_lst, "agg_sectors_lst.csv", YEAR)
         msg_lst.append(msg1)
      if (file_cat_det):
         rv, msg1=save_file(file_cat_det, "agg_sectors_det.csv", YEAR)
         msg_lst.append(msg1)
   else:
      msg_lst=[]

   return render_template("nav_inputCategory.html", msg_lst=msg_lst)   

# DB----------------------------------------------------------------------------
@app.route('/login')
def login():
   return redirect(url_for('nav_login', mode='prompt'))
    
@app.route('/nav_login/<mode>', methods=['GET', 'POST'])
def nav_login(mode):
   #return f"Hello nav_login {mode}"
   message=''; status=''
   if (mode == "prompt"):
      if request.method == 'POST' and 'userid' in request.form and 'password' in request.form:
         userid = request.form['userid']
         password = get_hash_password(request.form['password'])

         message, status = login_prompt(db, userid, password)
         if (status=="success"):
            return redirect(url_for('nav_home'))

      return render_template('nav_login.html', message=message, mode=mode, status=status)

   elif (mode=="register"):
      message=''; status=''
      if request.method == 'POST' and 'password' in request.form and 'password' in request.form and 'email' in request.form:
         userID = request.form['userid']
         userName = request.form['name']
         password = get_hash_password(request.form['password'])
         email = request.form['email']

         message, status = login_register(db, mail, userID, userName, password, email)
      elif request.method == 'POST':
         #print("fill in request form")
         message = 'Please fill out the form !'      
      return render_template('nav_login.html', message=message, mode=mode, status=status)

   elif (mode=="change_password"):
      message = ''; status = ''
      #print("inside change_password")
      if request.method == 'POST' and session['loggedin']:
         password_old = get_hash_password(request.form['password_old'])
         password_new = get_hash_password(request.form['password_new'])

         message, status = login_changePassword(db, password_old, password_new)

      return render_template('nav_login.html', message=message, mode=mode, status=status)

   elif (mode=="verify_user"):
      userid=request.args.get('userid')
      if (userid):
         print("userid", userid)
         message, status=verify_user(db, userid)

      df_user=get_table_user(db)
      tbl_user = df_user.to_dict(orient='records')

      return render_template('nav_login.html', mode=mode, tbl_user=tbl_user, message=message)

   elif (mode=="delete_user"):
      userid=request.args.get('userid')
      if (userid):
         print("userid", userid)
         message, status=delete_user(db, userid)

      df_user=get_table_user(db)
      tbl_user = df_user.to_dict(orient='records')

      return render_template('nav_login.html', mode=mode, tbl_user=tbl_user, message=message)

   elif (mode=="logout"):
      session.pop('loggedin', None)
      session.pop('userid', None)
      session.pop('email', None)
      return redirect(url_for('nav_login', mode='prompt'))

#LOGIN-MAIL---------------------------------------------------------------------------------------
@app.route("/verify_email/<token>")
def verify_email(token):
   message, status = verify_email_byToken(db, token)
   mode="register"
   return render_template('nav_login.html', message=message, mode=mode, status=status)


if __name__ == '__main__':
   app.run(debug=True)