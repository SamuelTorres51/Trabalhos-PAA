import csv
import time
import tracemalloc
from pathlib import Path


REPETICOES_TEMPO = 21


def contar_passos(caminho):
  if caminho is None:
    return None
  return len(caminho) - 1


def medir_tempo_medio(funcao, labirinto, repeticoes=REPETICOES_TEMPO):
  tempos = []
  for _ in range(repeticoes):
    inicio = time.perf_counter()
    funcao(labirinto)
    tempos.append(time.perf_counter() - inicio)
  return sum(tempos) / len(tempos)


def medir_memoria(funcao, labirinto):
  tracemalloc.start()
  resultado = funcao(labirinto)
  _, pico = tracemalloc.get_traced_memory()
  tracemalloc.stop()
  return pico, resultado


def _resultado_obtido(dados):
  if dados["passos"] is None:
    return "Sem solucao"
  return f"Caminho com {dados['passos']} passos"


def _melhor_solucao_encontrada(dados, otimo):
  if dados["passos"] is None:
    return "Nao encontrou"
  if dados["passos"] == otimo:
    return "Sim (otimo)"
  return f"Nao ({dados['passos'] - otimo} passos a mais)"


def salvar_csv(resultados, caminho_csv):
  caminho_csv = Path(caminho_csv)
  caminho_csv.parent.mkdir(parents=True, exist_ok=True)

  cabecalho = [
    "caso",
    "dimensao",
    "algoritmo",
    "resultado_obtido",
    "melhor_solucao_encontrada",
    "tempo_execucao_ms",
    "numero_de_decisoes",
    "memoria_pico_bytes",
  ]

  with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(cabecalho)

    for resultado in resultados:
      otimo = resultado["backtracking"]["passos"]
      linhas = len(resultado["labirinto"])
      colunas = len(resultado["labirinto"][0])
      dimensao = f"{linhas}x{colunas}"

      for rotulo, chave in (("Guloso", "guloso"), ("Backtracking", "backtracking")):
        dados = resultado[chave]
        escritor.writerow([
          resultado["nome"],
          dimensao,
          rotulo,
          _resultado_obtido(dados),
          _melhor_solucao_encontrada(dados, otimo),
          f"{dados['tempo'] * 1000:.4f}",
          dados["decisoes"],
          dados["memoria"],
        ])

  return caminho_csv
