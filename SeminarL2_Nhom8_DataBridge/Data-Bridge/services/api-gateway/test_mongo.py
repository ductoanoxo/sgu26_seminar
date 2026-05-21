import urllib.parse

def build_uri(username, password, host, port, database_name):
    enc_user = urllib.parse.quote_plus(username)
    enc_pass = urllib.parse.quote_plus(password)
    
    is_srv = "mongodb.net" in host
    protocol = "mongodb+srv" if is_srv else "mongodb"
    
    uri = f"{protocol}://{enc_user}:{enc_pass}@{host}"
    if not is_srv and port:
        uri += f":{port}"
        
    db_name = database_name if database_name and database_name != 'default' else "admin"
    uri += f"/{db_name}?retryWrites=true&w=majority&authSource=admin"
    return uri

print(build_uri("admin", "matkhau@", "cluster.mongodb.net", 27017, "default"))
