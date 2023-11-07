credentials ={
    "user_mongo": "admin",
    "password_mongo": "admin",
}

settings = {
    "host": "cidadealerta.2nltvs3.mongodb.net",
    "database": "db_cidade_alerta",
    "collection": "problemas",
    "port": "4800"
}


url = f"mongodb+srv://{credentials['user_mongo']}:{credentials['password_mongo']}@{settings['host']}/{settings['database']}?retryWrites=true&w=majority"
print(url)