from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, random, string

app = Flask(__name__)
CORS(app)

# ข้อมูลคีย์ชุดล่าสุดของคุณ
SECRET_KEY = "6LcavvArAAAAAAOWDD_1TaBUwCfnNH3sDSR1L5cV"
database = {} 

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    uid = str(data.get('userid'))
    token = data.get('token')
    
    verify = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': SECRET_KEY, 
        'response': token
    }).json()

    if verify.get('success'):
        # สร้างรหัส 6 หลักที่จำง่าย
        passkey = "SAN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        database[uid] = passkey
        return jsonify({"passkey": passkey})
    return jsonify({"error": "Captcha Invalid"}), 400

@app.route('/api/verify/<uid>/<key>')
def verify_script(uid, key):
    if uid in database and database[uid] == key:
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"}), 401

if __name__ == "__main__":
    # Render จะส่งตัวแปร PORT มาให้ ถ้าไม่มีให้ใช้ 10000
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
