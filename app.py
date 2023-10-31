from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from credentials_file import settings, credentials
from werkzeug.utils import secure_filename
import os 

UPLOAD_FOLDER = '/photos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb+srv://{credentials['user_mongo']}:{credentials['password_mongo']}@{settings['host']}/{settings['database']}?retryWrites=true&w=majority"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)

def allowed_foto(fotoname):
    return '.' in fotoname and \
           fotoname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas
@app.route("/problemas", methods=["GET"])
def get_problemas():
    try:
        filter_ = {}
        projection_ = {}
        problemas = list(mongo.db.problemas.find(filter_, projection_))
        for problema in problemas:
            problema["_id"] = str(problema["_id"])
        return {"problemas": problemas}, 200
    except Exception as e: 
        return {'erro': f'{e}'}

@app.route("/problemas", methods=["POST"])
def cadastro_problemas():
    try:
        data = request.data
        foto = request.files['foto']
        if foto and allowed_foto(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data['foto'] = filename
        if not all(k in data for k in ("rua", "bairro", "problema_tipo","urgencia","problema_descricao","data_inicio")):
            return jsonify({"erro": "Campos obrigatórios faltando!"}), 400
        problema_id = mongo.db.problemas.insert_one(data)
        print(problema_id.inserted_id)
        return {"_id": str(problema_id.inserted_id)}, 201
    except Exception as e: 
        return {'erro': f'{e}'}


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=4800)
