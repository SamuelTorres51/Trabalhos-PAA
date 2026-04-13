from csv import DictWriter
from pathlib import Path
from random import Random
from time import perf_counter
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
RESULTS_DIR = BASE_DIR / "results"
FILES_DIR = RESULTS_DIR / "files"
GRAPHICS_DIR = RESULTS_DIR / "graphics"
SEMENTE_BASE = 42
TAMANHOS_PADRAO = (20000, 40000, 60000)
ALGORITMOS = {
    "mergesort": None,
    "timsort": None,
}
TIPOS_CASO = ("crescente", "decrescente", "aleatorio")

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mergesort import mergesort
from timsort import timsort

ALGORITMOS["mergesort"] = mergesort
ALGORITMOS["timsort"] = timsort


def gerar_vetor_aleatorio(tamanho, semente=None):
    gerador = Random(semente)
    return [gerador.randint(0, tamanho * 10) for _ in range(tamanho)]


def contar_tempo(funcao_ordenacao, vetor):
    inicio = perf_counter()
    funcao_ordenacao(vetor)
    fim = perf_counter()
    return fim - inicio


def gerar_casos(tamanho, semente):
    vetor_crescente = list(range(tamanho))
    vetor_decrescente = list(range(tamanho, 0, -1))
    vetor_aleatorio = gerar_vetor_aleatorio(tamanho, semente)

    return {
        "crescente": vetor_crescente,
        "decrescente": vetor_decrescente,
        "aleatorio": vetor_aleatorio,
    }


def executar_benchmark(tamanhos=TAMANHOS_PADRAO):
    resultados = []

    for tamanho in tamanhos:
        casos = gerar_casos(tamanho, SEMENTE_BASE + tamanho)

        for nome_algoritmo, funcao_ordenacao in ALGORITMOS.items():
            for tipo_caso in TIPOS_CASO:
                vetor_base = casos[tipo_caso]
                tempo = contar_tempo(funcao_ordenacao, vetor_base[:])

                resultados.append(
                    {
                        "algoritmo": nome_algoritmo,
                        "tipo_caso": tipo_caso,
                        "tamanho": tamanho,
                        "tempo_segundos": tempo,
                    }
                )

    return resultados


def agrupar_resultados_por_algoritmo(resultados):
    agrupados = {nome: [] for nome in ALGORITMOS}
    for resultado in resultados:
        agrupados[resultado["algoritmo"]].append(resultado)
    return agrupados


def salvar_resultados_csv(caminho_arquivo, resultados):
    caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    with caminho_arquivo.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = DictWriter(
            arquivo,
            fieldnames=["algoritmo", "tipo_caso", "tamanho", "tempo_segundos"],
        )
        escritor.writeheader()
        escritor.writerows(resultados)


def salvar_resultados_por_algoritmo(resultados):
    agrupados = agrupar_resultados_por_algoritmo(resultados)
    for nome_algoritmo, itens in agrupados.items():
        caminho = FILES_DIR / nome_algoritmo / "tempos.csv"
        salvar_resultados_csv(caminho, itens)


def preparar_dados_para_grafico(resultados, algoritmo, tipo_caso):
    filtrados = [
        item for item in resultados
        if item["algoritmo"] == algoritmo and item["tipo_caso"] == tipo_caso
    ]
    filtrados.sort(key=lambda item: item["tamanho"])
    tamanhos = [item["tamanho"] for item in filtrados]
    tempos = [item["tempo_segundos"] for item in filtrados]
    return tamanhos, tempos


def criar_grafico_por_algoritmo(resultados, algoritmo):
    figura, eixo = plt.subplots(figsize=(10, 6))

    for tipo_caso in TIPOS_CASO:
        tamanhos, tempos = preparar_dados_para_grafico(resultados, algoritmo, tipo_caso)
        eixo.plot(tamanhos, tempos, marker="o", linewidth=2, label=tipo_caso.capitalize())

    eixo.set_title(f"Desempenho do {algoritmo.capitalize()}")
    eixo.set_xlabel("Quantidade de elementos")
    eixo.set_ylabel("Tempo de ordenacao (segundos)")
    eixo.grid(True, alpha=0.3)
    eixo.legend()
    figura.tight_layout()

    destino = GRAPHICS_DIR / algoritmo / f"desempenho_{algoritmo}.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=150)
    plt.close(figura)


def criar_grafico_comparativo(resultados):
    figura, eixos = plt.subplots(1, len(TIPOS_CASO), figsize=(18, 5), sharey=True)

    if len(TIPOS_CASO) == 1:
        eixos = [eixos]

    for eixo, tipo_caso in zip(eixos, TIPOS_CASO):
        for nome_algoritmo in ALGORITMOS:
            tamanhos, tempos = preparar_dados_para_grafico(resultados, nome_algoritmo, tipo_caso)
            eixo.plot(tamanhos, tempos, marker="o", linewidth=2, label=nome_algoritmo.capitalize())

        eixo.set_title(tipo_caso.capitalize())
        eixo.set_xlabel("Quantidade de elementos")
        eixo.grid(True, alpha=0.3)

    eixos[0].set_ylabel("Tempo de ordenacao (segundos)")
    eixos[-1].legend()
    figura.suptitle("Comparacao entre Mergesort e TimSort")
    figura.tight_layout(rect=[0, 0, 1, 0.95])

    destino = GRAPHICS_DIR / "comparativo" / "comparacao_algoritmos.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=150)
    plt.close(figura)


def gerar_graficos(resultados):
    for nome_algoritmo in ALGORITMOS:
        criar_grafico_por_algoritmo(resultados, nome_algoritmo)
    criar_grafico_comparativo(resultados)


def main():
    resultados = executar_benchmark()
    salvar_resultados_por_algoritmo(resultados)
    gerar_graficos(resultados)


if __name__ == "__main__":
    main()
