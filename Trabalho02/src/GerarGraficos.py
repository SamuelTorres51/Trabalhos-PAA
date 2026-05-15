# gerar_graficos.py

import pandas as pd  
import matplotlib.pyplot as plt
import os


# =========================================================
# CAMINHOS DOS CSVs
# =========================================================
caminho_recursivo = "../results/CaminhoMinimoRecursivo/resultados.csv"
caminho_dinamico = "../results/CaminhoMinimoDinamico/resultados.csv"

# Pasta onde os gráficos serão salvos
pasta_graficos = "../results/graficos"

os.makedirs(pasta_graficos, exist_ok=True)


# =========================================================
# LEITURA DOS DADOS
# =========================================================
dados_recursivo = pd.read_csv(caminho_recursivo)
dados_dinamico = pd.read_csv(caminho_dinamico)


# =========================================================
# GRÁFICO - TEMPO DE EXECUÇÃO
# =========================================================
plt.figure(figsize=(10, 6))

plt.plot(
    dados_recursivo["TamanhoMatriz"],
    dados_recursivo["TempoExecucao"],
    marker='o',
    label='Recursivo'
)

plt.plot(
    dados_dinamico["TamanhoMatriz"],
    dados_dinamico["TempoExecucao"],
    marker='o',
    label='Programação Dinâmica'
)

plt.xlabel("Tamanho da Matriz")
plt.ylabel("Tempo de Execução (segundos)")
plt.title("Tempo de Execução: Recursivo vs Programação Dinâmica")

plt.legend()
plt.grid(True)

plt.savefig(f"{pasta_graficos}/tempo_execucao.png")

plt.close()


# =========================================================
# GRÁFICO - MEMÓRIA CONSUMIDA
# =========================================================
plt.figure(figsize=(10, 6))

plt.plot(
    dados_recursivo["TamanhoMatriz"],
    dados_recursivo["MemoriaBytes"],
    marker='o',
    label='Recursivo'
)

plt.plot(
    dados_dinamico["TamanhoMatriz"],
    dados_dinamico["MemoriaBytes"],
    marker='o',
    label='Programação Dinâmica'
)

plt.xlabel("Tamanho da Matriz")
plt.ylabel("Memória Consumida (bytes)")
plt.title("Consumo de Memória: Recursivo vs Programação Dinâmica")

plt.legend()
plt.grid(True)

plt.savefig(f"{pasta_graficos}/memoria_consumida.png")

plt.close()


# =========================================================
# GRÁFICO - COMPARAÇÃO GERAL
# =========================================================
plt.figure(figsize=(10, 6))

plt.plot(
    dados_recursivo["TamanhoMatriz"],
    dados_recursivo["TempoExecucao"],
    marker='o',
    label='Tempo Recursivo'
)

plt.plot(
    dados_dinamico["TamanhoMatriz"],
    dados_dinamico["TempoExecucao"],
    marker='o',
    label='Tempo Dinâmico'
)

plt.xlabel("Tamanho da Matriz")
plt.ylabel("Tempo de Execução (segundos)")
plt.title("Comparação Geral de Desempenho")

plt.legend()
plt.grid(True)

plt.savefig(f"{pasta_graficos}/comparacao_geral.png")

plt.close()


print("Gráficos gerados com sucesso!")