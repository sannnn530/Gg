from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
import string

app = Flask(__name__)
CORS(app) # อนุญาตให้ Blogspot ส่งข้อมูลเข้ามาได้

# ใส่ Secret Key จากหน้า Google reCAPTCHA Admin ของคุณ
SECRET_KEY = "ใส่_SECRET_KEY_ของคุณที่นี่"
# ระบบเก็บข้อมูลชั่วคราว { "UserId": "Passkey" }
active_keys = {}

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    uid = str(data.get('userid'))
    token = data.get('token')

    # ตรวจสอบ Captcha กับ Google
    verify = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': SECRET_KEY,
        'response': token
    }).json()

    if verify.get('success'):
        # สร้าง Passkey แบบสุ่มล็อคกับ ID
        passkey = "SAN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        active_keys[uid] = passkey
        return jsonify({"passkey": passkey})
    
    return jsonify({"error": "Invalid"}), 400

@app.route('/api/verify/<uid>/<key>')
def verify_script(uid, key):
    # เช็คว่า ID ในเกมกับ Key ตรงกับที่ขอไว้ในเว็บไหม
    if uid in active_keys and active_keys[uid] == key:
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"}), 401
