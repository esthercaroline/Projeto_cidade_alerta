from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import credentials_file as credentials
app = Flask("Cidade Alerta")

# Conexão com o Mongo
con_string = f"mongodb+srv://{credentials['user_mongo']}:{credentials['password_mongo']}@cidadealerta.2nltvs3.mongodb.net/"
client = MongoClient(con_string)

col_problemas = client.db_cidade_alerta.problemas

# Rotas
@app.route("/problemas", methods=["GET"])
def get_problemas():
    problemas = col_problemas.find()
    return jsonify(problemas)

