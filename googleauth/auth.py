import os
import requests
import json

from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from flask import Flask, request, redirect, session, render_template, request
import flask
from PIL import Image
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

with open("auth_google.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(20)
app.config['UPLOAD_FOLDER'] = 'uploads/'

google_auth = GoogleClient(
    client_id=data['web']["client_id"],
    client_secret=data['web']["client_secret"],
    redirect_uri="http://localhost:8080/google/oauth2callback",
)

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/google/")
def google_index():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
        
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/oauth2/v2/userinfo")
        
    r.raise_for_status()
    user_data = r.json()
    return f"Hello, {user_data.get('name')}!"

@app.route("/google/oauth2callback")
def google_oauth2callback():
    code = request.args.get("code")
    error = request.args.get("error")
    
    if error:
        return f"Error: {error}"
        
    if not code:
        return redirect(google_auth.authorize_url(
            scope=SCOPES,
            response_type="code",
        ))
        
    auth_data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    
    session["access_token"] = auth_data.get("access_token")
    return redirect("/")

@app.route('/upload/', methods=['POST'])
def upload():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
    if 'files[]' not in request.files:
        return 'Нет файлов, выбранных для загрузки.'
    files = request.files.getlist('files[]')
    images = []
    for file in files:
           if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            images.append(file_path)
    if len(images) != 0:
        pdf_path = create_pdf(images)
        return flask.send_file(pdf_path, as_attachment=True)
    else:
        return "Неизвестный формат файла"

@app.route("/logout", methods=["GET", "POST"])
def logout():   
    session.clear()    
    return redirect("/")

"""def create_pdf(images):
    ls = []
    for file in images:
        file = Image.open(file)
        file.save('output.pdf', save_all=True, append_images=[*ls])
        ls.append(file)
    file = 'output.pdf'
    return file
    os.rmdir('/uploads/')"""
"""def create_pdf(images):
    pil_images = []

    for path in images:
        img = Image.open(path).convert("RGB")
        pil_images.append(img)

    pdf_path = "output.pdf"

    if not pil_images:
        return None

    first_image = pil_images[0]
    rest_images = pil_images[1:]

    first_image.save(pdf_path, save_all=True, append_images=rest_images)
    return pdf_path"""
def create_pdf(images):
    pdf_path = "output.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    for path in images:
        img = Image.open(path).convert("RGB")
        img_reader = ImageReader(img)

        iw, ih = img.size
        scale = min(width / iw, height / ih)
        dw, dh = iw * scale, ih * scale
        x = (width - dw) / 2
        y = (height - dh) / 2

        c.drawImage(img_reader, x, y, dw, dh)
        c.showPage()

    c.save()
    return pdf_path

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif']
    if filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
   

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host="localhost", port=8080)