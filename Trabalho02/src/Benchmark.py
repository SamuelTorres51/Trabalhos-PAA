# benchmark.py

import time
import tracemalloc
import random
import csv
import os

from CaminhoRecursivo import caminho_minimo_recursivo
from CaminhoDinamico import caminho_minimo_dinamico


# =========================================================
# GERA MATRIZ ALEATÓRIA
# =========================================================
def gerar_matriz(tamanho, valor_min=1, valor_max=9):
    return [
        [random.randint(valor_min, valor_max) for _ in range(tamanho)]
        for _ in range(tamanho)
    ]


# =========================================================
# MEDE TEMPO E MEMÓRIA
# =========================================================
def medir_desempenho(funcao, matriz):

    tracemalloc.start()

    inicio = time.perf_counter()

    resultado = funcao(matriz)

    fim = time.perf_counter()

    memoria_atual, pico_memoria = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    tempo_execucao = fim - inicio

    return tempo_execucao, pico_memoria, resultado


# =========================================================
# SALVA RESULTADOS EM CSV
# =========================================================
def salvar_csv(caminho_arquivo, dados):

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:

        writer = csv.writer(arquivo)

        writer.writerow([
            "TamanhoMatriz",
            "TempoExecucao",
            "MemoriaBytes",
            "Resultado"
        ])

        writer.writerows(dados)


# =========================================================
# EXECUTA TESTES
# =========================================================
def executar_benchmark():

    # Cenários de teste
    tamanhos = [5, 7, 9, 11, 13]

    resultados_recursivo = []
    resultados_dinamico = []

    print("\n========== INICIANDO BENCHMARK ==========\n")

    for tamanho in tamanhos:

        print(f"Executando testes para matriz {tamanho}x{tamanho}")

        matriz = gerar_matriz(tamanho)

        # -------------------------------------------------
        # RECURSIVO
        # -------------------------------------------------
        tempo_rec, memoria_rec, resultado_rec = medir_desempenho(
            caminho_minimo_recursivo,
            matriz
        )

        resultados_recursivo.append([
            tamanho,
            tempo_rec,
            memoria_rec,
            resultado_rec
        ])

        print("Recursivo finalizado")

        # -------------------------------------------------
        # DINÂMICO
        # -------------------------------------------------
        tempo_din, memoria_din, resultado_din = medir_desempenho(
            caminho_minimo_dinamico,
            matriz
        )

        resultados_dinamico.append([
            tamanho,
            tempo_din,
            memoria_din,
            resultado_din
        ])

        print("Dinâmico finalizado\n")

    # =====================================================
    # SALVANDO CSVs
    # =====================================================

    salvar_csv(
        "../results/CaminhoMinimoRecursivo/resultados.csv",
        resultados_recursivo
    )

    salvar_csv(
        "../results/CaminhoMinimoDinamico/resultados.csv",
        resultados_dinamico
    )

    print("========== BENCHMARK FINALIZADO ==========")


# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================
if __name__ == "__main__":
    executar_benchmark()