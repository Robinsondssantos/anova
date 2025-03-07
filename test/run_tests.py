import asyncio
import time
import aiohttp
import requests
import numpy as np
from scipy.stats import ttest_ind
import csv
import matplotlib.pyplot as plt

async def requisicao_api(session, url):
    inicio = time.time()
    async with session.get(url) as resposta:
        await resposta.read()  # Aguarda a resposta completa
    fim = time.time()
    return fim - inicio

async def executar_testes(url, numero_requisicoes):
    tempos_resposta = []
    async with aiohttp.ClientSession() as session:
        for _ in range(numero_requisicoes):
            tempo = await requisicao_api(session, url)
            tempos_resposta.append(tempo)
    return tempos_resposta

def teste_hipoteses(tempos_api1, tempos_api2, alpha):
    # Teste t de Student para amostras independentes
    estatistica_t, valor_p = ttest_ind(tempos_api1, tempos_api2)
    print(f"Estatística t: {estatistica_t}")
    print(f"Valor p: {valor_p}")

    if valor_p < alpha:
        print("Rejeitamos a hipótese nula. Há diferença significativa entre os tempos de resposta.")
    else:
        print("Não rejeitamos a hipótese nula. Não há evidência de diferença significativa entre os tempos de resposta.")

def salvar_resultados_csv(tempos_api1, tempos_api2, nome_arquivo):
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(['API', 'Tempo de Resposta'])
        for tempo in tempos_api1:
            writer.writerow(['API 1', tempo])
        for tempo in tempos_api2:
            writer.writerow(['API 2', tempo])

def gerar_grafico(tempos_api1, tempos_api2, nome_arquivo):
    plt.plot(tempos_api1, label='API com Corrotina')
    plt.plot(tempos_api2, label='API com Thread')
    plt.xlabel('Requisição')
    plt.ylabel('Tempo de Resposta (s)')
    plt.title('Comparação de Tempos de Resposta das APIs')
    plt.legend()
    plt.savefig(nome_arquivo)

if __name__ == '__main__':
    url_api1 = 'http://127.0.0.1:5001/api/pow'  # URL da API com corrotina
    url_api2 = 'http://127.0.0.1:5002/api/pow'  # URL da API com thread
    numero_requisicoes = 100  # Número de requisições para cada API
    alpha = 0.05  # Nível de significância

    print("Executando testes na API com corrotina...")
    tempos_api1 = asyncio.run(executar_testes(url_api1, numero_requisicoes))

    print("Executando testes na API com thread...")
    tempos_api2 = asyncio.run(executar_testes(url_api2, numero_requisicoes))

    print("\nResultados:")
    print(f"Tempos de resposta API 1: {tempos_api1}")
    print(f"Tempos de resposta API 2: {tempos_api2}")

    teste_hipoteses(tempos_api1, tempos_api2, alpha)

    nome_arquivo_csv = 'tempos_resposta.csv'
    salvar_resultados_csv(tempos_api1, tempos_api2, nome_arquivo_csv)
    print(f"Resultados salvos em {nome_arquivo_csv}")

    nome_arquivo_grafico = 'grafico_tempos_resposta.png'
    gerar_grafico(tempos_api1, tempos_api2, nome_arquivo_grafico)
    print(f"Gráfico salvo em {nome_arquivo_grafico}")