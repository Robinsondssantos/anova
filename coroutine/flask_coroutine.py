import asyncio
import hashlib
import time
from flask import Flask

app = Flask(__name__)

def prova_de_trabalho(dificuldade):
    numero = 0
    while True:
        hash_resultado = hashlib.sha256(str(numero).encode()).hexdigest()
        if hash_resultado.startswith('0' * dificuldade):
            return numero
        numero += 1

@app.route('/api/pow')
async def coroutine_api():
    dificuldade = 4  # Ajuste a dificuldade da PoW
    resultado = prova_de_trabalho(dificuldade)
    return {'message': 'Resposta da API com corrotina', 'resultado': resultado}

if __name__ == '__main__':
    app.run(debug=True, port=5001)