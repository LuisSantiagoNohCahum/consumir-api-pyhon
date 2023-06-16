#Importamos librerias necesarias
import time
import requests
import json

#Clase name para deserializar el objeto nombre que esta anidado en el objeto usuario
class Name:
    def __init__(self, title, first, last): #Constructor de la clase Name
        self.title = title
        self.first = first
        self.last = last

    def __iter__(self):
        yield from {
            "title": self.title,
            "first": self.first,
            "last": self.last
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

#Clase usuario para deserializar los datos de cada registro del json
class User:
    def __init__(self, gender, name, email, phone, cell, nat): #Constructor de la clase User
        self.gender = gender
        self.name = name
        self.email = email
        self.phone = phone
        self.cell = cell
        self.nat = nat

    def __iter__(self):
        yield from {
            "gender": self.gender,
            "name": self.name.__dict__,
            "email": self.email,
            "phone": self.phone,
            "cell": self.cell,
            "nat": self.nat
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
    #Metodo que permite deserializar cada registro del json a un objeto de de la clase User
    @staticmethod
    def from_json(json_dct):
        if 'gender' in json_dct.keys():
            Names= Name(**json_dct['name']) #Creacion del objeto Names de la clase Name
            return User(gender=json_dct['gender'], name=Names, email=json_dct['email'], phone=json_dct['phone'], cell=json_dct['cell'],nat=json_dct['nat'] )
        else:
            return json_dct


if __name__ == "__main__":
    #consumir api
    response = requests.get("https://randomuser.me/api/?inc=gender,name,email,phone,cell,nat&results=5000")
    start_time = time.perf_counter()
    # Aqui se usa la clase User para deserializar
    user_decoded = json.loads(response.text, object_hook=User.from_json)   
    list_users = list(user_decoded['results'])
    rows = 0
    for user in list_users: # Recorer los objeto deserializados
        if rows<=999:
            print("Usuario", (rows),
                        "\nGenero:", user.gender,
                        "\nNombre:",
                        "\n  Title:",user.name.title,
                        "\n  First:", user.name.first,
                        "\n  Last:", user.name.last,
                        "\nEmail:",user.email,
                        "\nPhone:",user.phone,
                        "\nCell:",user.cell,
                        "\nNacionalidad:",user.nat,"\n")
            rows = rows + 1
        else: break #salir apenas se alcancen e impriman los primeros 1000 registros
        
        #tiempo
    time_execution = time.perf_counter() - start_time

    print(f"{rows} registros recuperados en {time_execution} segundos")
    