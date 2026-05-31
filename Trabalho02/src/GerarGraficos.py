# gerar_graficos.py

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# =========================================================
# CAMINHOS DOS CSVs
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR.parent / "results"

caminho_comparativo = RESULTS_DIR / "comparativo_geral.csv"

# Pasta onde os gráficos serão salvos
pasta_graficos = RESULTS_DIR / "graficos"

pasta_graficos.mkdir(parents=True, exist_ok=True)

for arquivo_png in pasta_graficos.glob("*.png"):
    arquivo_png.unlink()


# =========================================================
# LEITURA DOS DADOS
# =========================================================
dados = pd.read_csv(caminho_comparativo)
dados = dados.sort_values(["Cenario", "Versao"])

ordem_versao = {"Recursivo": 0, "Programação Dinâmica": 1}


def gerar_slug(texto):
    return texto.lower().replace(" ", "_")


def gerar_grafico_por_cenario(nome_cenario, dados_cenario):
    dados_ordenados = dados_cenario.sort_values(
        "Versao",
        key=lambda serie: serie.map(ordem_versao)
    )
    versoes = dados_ordenados["Versao"].tolist()
    tempos = dados_ordenados["TempoExecucao"].tolist()
    memorias = dados_ordenados["MemoriaEstimativaBytes"].tolist()

    figura, eixos = plt.subplots(1, 2, figsize=(12, 5))
    figura.suptitle(f"Desempenho por Cenário: {nome_cenario}")

    eixos[0].bar(versoes, tempos, color=["#2E86AB", "#F18F01"])
    eixos[0].set_title("Tempo de Execução")
    eixos[0].set_ylabel("Segundos")
    eixos[0].grid(axis="y", alpha=0.3)

    eixos[1].bar(versoes, memorias, color=["#2E86AB", "#F18F01"])
    eixos[1].set_title("Memória Consumida")
    eixos[1].set_ylabel("Bytes")
    eixos[1].grid(axis="y", alpha=0.3)

    for eixo, valores in zip(eixos, [tempos, memorias]):
        for indice, valor in enumerate(valores):
            eixo.text(indice, valor, f"{valor:.6f}" if eixo is eixos[0] else f"{int(valor)}",
                      ha="center", va="bottom", fontsize=9)

    figura.tight_layout(rect=[0, 0, 1, 0.95])
    figura.savefig(pasta_graficos / f"{gerar_slug(nome_cenario)}_comparativo.png")
    plt.close(figura)


def gerar_grafico_metricas_por_cenario(nome_cenario, dados_cenario):
    dados_ordenados = dados_cenario.sort_values(
        "Versao",
        key=lambda serie: serie.map(ordem_versao)
    )
    versoes = dados_ordenados["Versao"].tolist()
    tempos = dados_ordenados["TempoExecucao"].tolist()
    memorias = dados_ordenados["MemoriaEstimativaBytes"].tolist()

    for titulo, valores, arquivo_saida, rotulo_y, cores in [
        (
            "Tempo de Execução",
            tempos,
            f"{gerar_slug(nome_cenario)}_tempo_execucao.png",
            "Segundos",
            ["#2E86AB", "#F18F01"],
        ),
        (
            "Memória Consumida",
            memorias,
            f"{gerar_slug(nome_cenario)}_memoria_consumida.png",
            "Bytes (estimativa)",
            ["#5B8E7D", "#D96C75"],
        ),
    ]:
        figura, eixo = plt.subplots(figsize=(8, 5))
        figura.suptitle(f"{nome_cenario} - {titulo}")

        eixo.bar(versoes, valores, color=cores)
        eixo.set_ylabel(rotulo_y)
        eixo.grid(axis="y", alpha=0.3)

        for indice, valor in enumerate(valores):
            eixo.text(
                indice,
                valor,
                f"{valor:.6f}" if titulo == "Tempo de Execução" else f"{int(valor)}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        figura.tight_layout(rect=[0, 0, 1, 0.94])
        figura.savefig(pasta_graficos / arquivo_saida)
        plt.close(figura)


# =========================================================
# GERA GRAFICOS POR CENARIO
# =========================================================
for nome_cenario, dados_cenario in dados.groupby("Cenario"):
    gerar_grafico_por_cenario(nome_cenario, dados_cenario)
    gerar_grafico_metricas_por_cenario(nome_cenario, dados_cenario)


print("Gráficos gerados com sucesso!")