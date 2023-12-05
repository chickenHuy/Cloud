import login as lg
from flask import *
import getfile
import uploadfile
import deletefile
import downloadfile

app = Flask(__name__) 

@app.route('/submit', methods=['POST'])
def submit():
    access_key_id = request.form['access_key_id']
    secret_access_key = request.form['secret_access_key']
    
    if lg.login_authentication(access_key_id, secret_access_key):
        print(f'Success')
        print(f'AWS Access Key ID: {access_key_id}')
        print(f'AWS Secret Access Key: {secret_access_key}')
        session['login'] = True
        session['access_key_id'] = access_key_id
        session['secret_access_key'] = secret_access_key
        status = 'True'
        return jsonify({'status': status})
    else:
        print(f'False')
        status = 'False'
        return jsonify({'status': status})

@app.route('/home')
def home():
    if 'login' not in session: 
        return redirect('/')
    if 'login' in session and session['login'] != True:
        return redirect('/')
        
    json_files = getfile.get_file()
    if json_files:
        session['json_files'] = json_files
    return render_template('home.html', json_files=json_files)

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json() 
    index = data.get('index') 
    file = data.get('file') 

    message = deletefile.delete_file(session['access_key_id'], session['secret_access_key'], file)

    if message != "":
        print(message)
        print()
        status = 'True'
        return jsonify({'status': status, 'message': message})
    else:
        print('Delete error!!!')
        status = 'False'
        return jsonify({'status': status, 'message': 'Failed to delete file'})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json() 
    file = data.get('file') 
    message = downloadfile.download_file(session['access_key_id'], session['secret_access_key'], "awsbucket-project", file)
    if message != "":
        status = 'True'
        print(message)
        print()
        return jsonify({'status': status, 'message': message})
    else:
        print('Download error!!!')
        status = 'False'
        return jsonify({'status': status, 'message': 'Failed to download file'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    message = uploadfile.upload_file_to_s3(file, session['access_key_id'], session['secret_access_key'], session['folder_name'])
    if message != "":
        status = 'True'
        print(message)
        print()
        return jsonify({'status': status, 'message': message})
    else:
        print('Upload error!!!')
        status = 'False'
        return jsonify({'status': status, 'message': 'Failed to download file'})

@app.route('/logout')
def logout():
    if 'login' in session and session['login'] == True:
        session.clear()
        print('Cooooooooo')
        redirect('/')
    return redirect('/')

@app.route('/')
def login():
    return render_template('index.html')

if __name__=='__main__': 
    app.secret_key = 'super secret key'
    app.run() 
