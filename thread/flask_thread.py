import hashlib
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

def prova_de_trabalho(dificuldade):
    numero = 0
    while True:
        hash_resultado = hashlib.sha256(str(numero).encode()).hexdigest()
        if hash_resultado.startswith('0' * dificuldade):
            return numero
        numero += 1

def process_request(dificuldade):
    resultado = prova_de_trabalho(dificuldade)
    return {'message': 'Resposta da API com thread', 'resultado': resultado}

@app.route('/api/pow')
def thread_api():
    dificuldade = 4  # Ajuste a dificuldade da PoW
    thread = Thread(target=process_request, args=(dificuldade,))
    thread.start()
    thread.join()  # Espera a thread terminar
    return process_request(dificuldade)

if __name__ == '__main__':
    app.run(debug=True, port=5002)