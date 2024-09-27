def db_init(app):
    from flask_mysqldb import MySQL

    app.secret_key = '__eeio__'

    # Set MySQL data
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'db_eeio'

    #note: check services.msc in Windows to see if MySQL is running

    mysql = MySQL(app)
    return mysql

def get_hash_password(password):
    #https://pagorun.medium.com/password-encryption-in-python-securing-your-data-9e0045e039e1
    import hashlib

    hash_object = hashlib.sha256()# Convert the password to bytes and hash it
    hash_object.update(password.encode())# Get the hex digest of the hash
    hash_password = hash_object.hexdigest()
    #print(hash_password)

    return hash_password 