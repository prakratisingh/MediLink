from flask import Flask,redirect, render_template, request, url_for, session
from flask_session import Session
import os
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from werkzeug.utils import secure_filename
from data import DataBase
from bchain import MedBlockchain
from datetime import date
from transformers import utils
utils.logging.set_verbosity_error()

# Initialize Flask app
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

path = " "
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('model')


db = DataBase()
medchain = MedBlockchain()


@app.route('/')
def login():    
    return render_template('login.html')

@app.route('/login_authenticate',methods=['POST'])
def login_authenticate():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if db.authenticateUser(email,password) == True:
            session["name"] = request.form['email']
            return redirect(url_for('home'))
        else:
            return render_template('faillogin.html')

@app.route('/register_authenticate',methods=['POST','GET'])
def register_authenticate():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if db.insertUser(email,password,'') == False:
            return render_template('failregister.html')
        else:
            session["name"] = request.form.get("name")
            return redirect(url_for('home'))


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home',methods=['POST','GET'])
def home():
    if not session.get("name"):
        return redirect("/")
    return render_template('home.html')

@app.route('/upload',methods=['POST','GET'])
def upload():
    if not session.get("name"):
        return redirect("/")
    return render_template("upload.html")


@app.route('/process', methods=['POST'])
def process_image():
    if not session.get("name"):
        return redirect("/")
    if request.method=='POST':
        # form_data = request.form
        f = request.files['file1']
        img_path = os.path.join(path,secure_filename(f.filename))
        f.save(img_path)

        img = Image.open(img_path).convert("RGB")
        pixel_values = processor(images=img, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return render_template('saveData.html',generatedtext=generated_text)
    else:
        return render_template('upload.html')
    
@app.route('/savedata',methods=['POST'])
def savedata():
    if not session.get("name"):
        return redirect("/")
    medicine = str(request.form['gentext'])
    today = date.today().strftime('%d-%m-%Y')
    username = session['name']
    
    lastHash = medchain.createBlock(username=username,medicine=medicine,date=today)
    db.updateHash(username,lastHash)

    return render_template('successsave.html')

@app.route('/showdata',methods=['GET'])
def showdata():
    username = session['name']
    lastHash = db.last_hash(username)
    if len(lastHash)==0:
        return render_template('nodata.html')
    else:
        if medchain.checkIntegrity(username,lastHash) == True:
            userdata = medchain.getUserBlocks(username)
            return render_template('showdata.html',logged_in_user=username,user_data = userdata)
        else:
            return render_template('notsecure.html')

@app.route('/logout')
def logout():
    if not session.get("name"):
        return redirect("/")
    session['name'] = None
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')