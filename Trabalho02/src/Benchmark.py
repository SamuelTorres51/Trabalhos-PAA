import csv
import random
import sys
import time
from pathlib import Path

from CaminhoRecursivo import caminho_minimo_recursivo
from CaminhoDinamico import caminho_minimo_dinamico


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR.parent / "results"

SCENARIOS = [
  ("Cenario A", 8),
  ("Cenario B", 13),
]

NUM_EXECUCOES = 30
TAMANHO_FRAME_ESTIMADO = sys.getsizeof(sys._getframe())
TAMANHO_INTEIRO_ESTIMADO = sys.getsizeof(0)


def gerar_matriz(tamanho, rng, valor_min=1, valor_max=9):
  return [
    [rng.randint(valor_min, valor_max) for _ in range(tamanho)]
    for _ in range(tamanho)
  ]


def medir_desempenho(funcao, matriz):
  inicio = time.perf_counter()

  resultado = funcao(matriz)

  fim = time.perf_counter()

  tempo_execucao = fim - inicio

  return tempo_execucao, resultado


def medir_media_desempenho(funcao, matriz, num_execucoes=NUM_EXECUCOES):
  tempo_execucao, resultado = medir_desempenho(funcao, matriz)
  tempos = [tempo_execucao]

  for _ in range(num_execucoes - 1):
    tempo_execucao, resultado = medir_desempenho(funcao, matriz)
    tempos.append(tempo_execucao)

  return sum(tempos) / len(tempos), resultado


def estimar_memoria_recursiva(tamanho):
  profundidade_maxima = (2 * tamanho) - 1

  return profundidade_maxima * TAMANHO_FRAME_ESTIMADO


def estimar_memoria_dinamica(tamanho):
  memoria_estrutura = sys.getsizeof([None] * tamanho)
  memoria_estrutura += tamanho * sys.getsizeof([None] * tamanho)

  memoria_dados = tamanho * tamanho * TAMANHO_INTEIRO_ESTIMADO

  return memoria_estrutura + memoria_dados


def salvar_csv(caminho_arquivo, dados, cabecalho):
  caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

  with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
    writer = csv.writer(arquivo)

    writer.writerow(cabecalho)

    writer.writerows(dados)


def executar_benchmark():
  resultados_recursivo = []
  resultados_dinamico = []
  tabela_comparativa = []

  print("\n========== INICIANDO BENCHMARK ==========\n")

  for indice, (cenario, tamanho) in enumerate(SCENARIOS, start=1):
    print(f"Executando testes para {cenario} ({tamanho}x{tamanho})")

    rng = random.Random(1000 + indice)
    matriz = gerar_matriz(tamanho, rng)

    tempo_rec, (custo_rec, caminho_rec) = medir_media_desempenho(caminho_minimo_recursivo, matriz)

    memoria_rec = estimar_memoria_recursiva(tamanho)

    resultados_recursivo.append([
      cenario,
      tamanho,
      NUM_EXECUCOES,
      tempo_rec,
      memoria_rec,
      custo_rec
    ])

    tabela_comparativa.append([
      cenario,
      tamanho,
      NUM_EXECUCOES,
      "Recursivo",
      tempo_rec,
      memoria_rec,
      custo_rec
    ])

    print("Recursivo finalizado")
    print("Caminho:", " -> ".join(str(p) for p in caminho_rec))

    tempo_din, (custo_din, caminho_din) = medir_media_desempenho(caminho_minimo_dinamico, matriz)

    memoria_din = estimar_memoria_dinamica(tamanho)

    resultados_dinamico.append([
      cenario,
      tamanho,
      NUM_EXECUCOES,
      tempo_din,
      memoria_din,
      custo_din
    ])

    tabela_comparativa.append([
      cenario,
      tamanho,
      NUM_EXECUCOES,
      "Programação Dinâmica",
      tempo_din,
      memoria_din,
      custo_din
    ])

    print("Dinâmico finalizado")
    print("Caminho:", " -> ".join(str(p) for p in caminho_din), "\n")

  cabecalho = [
    "Cenario",
    "TamanhoMatriz",
    "Execucoes",
    "TempoExecucao",
    "MemoriaEstimativaBytes",
    "Resultado"
  ]

  salvar_csv(
    RESULTS_DIR / "CaminhoMinimoRecursivo" / "resultados.csv",
    resultados_recursivo,
    cabecalho
  )

  salvar_csv(
    RESULTS_DIR / "CaminhoMinimoDinamico" / "resultados.csv",
    resultados_dinamico,
    cabecalho
  )

  salvar_csv(
    RESULTS_DIR / "comparativo_geral.csv",
    tabela_comparativa,
    [
      "Cenario",
      "TamanhoMatriz",
      "Execucoes",
      "Versao",
      "TempoExecucao",
      "MemoriaEstimativaBytes",
      "Resultado"
    ]
  )

  print("========== BENCHMARK FINALIZADO ==========")


if __name__ == "__main__":
  executar_benchmark()
