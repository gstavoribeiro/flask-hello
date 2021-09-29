import os
import json
import pickle
import requests
import sklearn
from flask import Flask, render_template, request

app =  Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
  try:
    #receber o arquivo do formulário
    file = request.files['file
    
    #enviar o arquivo para a API
    response = requests.post(
      'https://face.ifelseonline.com.br/encoding',
      files = {'file':(
        file.filename,
        file.stream,
        file.content_type,
        file.headers
      )}
    )

    #decodificar resposta
    data = json.loads(response.text)

    #verificar se a resposta teve sucesso
    if not data['success']:
      return render_template(
        'predict.html', 
        predict='Sem faces'
      )

    #enviar as caracteristicas para o modelo
    face_encoding = data['encodings']
    clf = pickle.load(open('clf.pickle', 'rb'))
    predict = clf.predict([face_encoding])[0]

  except Exception:

    return render_template(
      'predict.html',
      predict='Erro ao reconhecer face'
    )
  
  return render_template(
    'predict.html',
    predict=predict
  )


  
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)