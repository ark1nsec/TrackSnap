# code by Ark1n https://github.com/ark1nsec
# create 25/04/2023
# contact ark1n@outlook.com.br

import cv2
import json
import datetime
import requests
from flask import Flask, render_template

app = Flask(__name__)

class createReport:

    def getData():
        # Pega a data e hora atual
        now = datetime.datetime.now()
        # Formatando a data e hora como uma string
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        return timestamp

    def getWebCamImage():
        # Nomeando o arquivo com a data e hora atual
        filename = f"SCREEN_{createReport.getIP()+'-'+createReport.getData()}.png"
        # Capturar a imagem da webcam
        captura = cv2.VideoCapture(0)
        # Ler um frame da captura
        ret, frame = captura.read()
        # Salvar a imagem em um arquivo
        cv2.imwrite(filename, frame)
        # Liberar a captura da webcam
        captura.release()
        # Seta template

    def getIP():
        # Coleta IP
        response = requests.get('https://api.ipify.org/?format=json').json()
        # Retorna IP
        return response["ip"]

    def getLocationIP():
        # Nomeando o arquivo com a data e hora atual
        filename = f"LOCATION_IP_{createReport.getIP()+'-'+createReport.getData()}.json"
        # Recupera IP do Usuáio
        ip_address = createReport.getIP()
        # Faz requisição para verificação
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        # Recupera retorno
        response = requests.get(request_url)
        # Decodifica e ajusta saida
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result  = json.loads(result)
        # Joga resultado para arquivo
        with open(filename,'w') as f:
            f.write(json.dumps(result,indent=4))
        
# Cria rota
@app.route("/")
def homepage():
    createReport.getWebCamImage()
    createReport.getLocationIP()
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)