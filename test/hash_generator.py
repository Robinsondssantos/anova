import hashlib

def prova_de_trabalho(dificuldade):
    numero = 0
    while True:
        hash_resultado = hashlib.sha256(str(numero).encode()).hexdigest()
        if hash_resultado.startswith('0' * dificuldade):
            print(hash_resultado)
            return numero
        print(hash_resultado)
        numero += 1

if __name__ == '__main__':
    prova_de_trabalho(4)