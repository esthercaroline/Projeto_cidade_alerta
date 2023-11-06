from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from credentials_file import settings, credentials
from werkzeug.utils import secure_filename
import os 


UPLOAD_FOLDER = 'static/photos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
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
        foto = request.files['foto']
        if foto and allowed_foto(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data_dict = {
            "bairro": request.form.get('bairro'),
            "rua": request.form.get('rua'),
            "problema_tipo": request.form.get('problema_tipo'),
            "urgencia": request.form.get('urgencia'),
            "problema_descricao": request.form.get('problema_descricao'),
            "data_inicio": request.form.get('data_inicio'),
            "foto": filename,  # Nome do arquivo da foto
            "status":"Em Análise",
            "latitude":request.form.get('latitude'),
            "longitude":request.form.get('longitude')
        }

        if not all(k in data_dict for k in ("bairro", "rua", "problema_tipo", "urgencia", "problema_descricao", "data_inicio", "foto","status","latitude","longitude")):
            return jsonify({"erro": "Campos obrigatórios faltando!"}), 400
        if filename == '':
            return jsonify({"erro": "Foto não enviada!"}), 400
        
        if isinstance(data_dict, dict):
            problema_id = mongo.db.problemas.insert_one(data_dict)
            return {"_id": str(problema_id.inserted_id)}, 201
        else:
            return jsonify({"erro": "Dados inválidos"}), 400

    except Exception as e: 
        return {'erro': f'{e}'}

@app.route("/problemas/filter", methods=["GET"])
def get_problemas_filter():
    try:
        filter_ = request.json
        if '_id' in filter_:
            filter_['_id'] = ObjectId(filter_['_id'])
        projection_ = {}
        problemas = list(mongo.db.problemas.find(filter_, projection_))
        for problema in problemas:
            problema["_id"] = str(problema["_id"])
        return {"problemas": problemas}, 200
    except Exception as e: 
        return {'erro': f'{e}'}

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=4800)
