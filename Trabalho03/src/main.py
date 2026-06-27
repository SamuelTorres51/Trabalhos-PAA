from pathlib import Path

import algoritmo_guloso
import algoritmo_backtracking
import gerador_labirinto
import gerar_imagem
import relatorio


PASTA_IMAGENS = Path(__file__).resolve().parent / "imagens"
CAMINHO_CSV = Path(__file__).resolve().parent / "metricas.csv"

SEMENTE = 7
TAMANHOS = [6, 8, 10, 12]


def construir_casos():
  casos = []
  for indice, tamanho in enumerate(TAMANHOS):
    labirinto = gerador_labirinto.gerar_labirinto(tamanho, semente=SEMENTE + indice)
    casos.append({
      "nome": f"Caso {indice + 1} - Labirinto {tamanho}x{tamanho}",
      "labirinto": labirinto,
    })
  return casos


def executar_caso(caso):
  labirinto = caso["labirinto"]

  pico_guloso, (caminho_guloso, decisoes_guloso, percorrido_guloso) = relatorio.medir_memoria(
    algoritmo_guloso.resolver, labirinto
  )
  tempo_guloso = relatorio.medir_tempo_medio(algoritmo_guloso.resolver, labirinto)

  pico_bt, (caminho_bt, decisoes_bt, _) = relatorio.medir_memoria(
    algoritmo_backtracking.resolver, labirinto
  )
  tempo_bt = relatorio.medir_tempo_medio(algoritmo_backtracking.resolver, labirinto)

  return {
    "nome": caso["nome"],
    "labirinto": labirinto,
    "guloso": {
      "caminho": caminho_guloso,
      "percorrido": percorrido_guloso,
      "passos": relatorio.contar_passos(caminho_guloso),
      "decisoes": decisoes_guloso,
      "tempo": tempo_guloso,
      "memoria": pico_guloso,
    },
    "backtracking": {
      "caminho": caminho_bt,
      "passos": relatorio.contar_passos(caminho_bt),
      "decisoes": decisoes_bt,
      "tempo": tempo_bt,
      "memoria": pico_bt,
    },
  }


def main():
  resultados = [executar_caso(caso) for caso in construir_casos()]

  caminho_csv = relatorio.salvar_csv(resultados, CAMINHO_CSV)
  gerar_imagem.gerar_imagens(resultados, PASTA_IMAGENS)

  print(f"Metricas salvas em: {caminho_csv}")
  print(f"Imagens salvas em:  {PASTA_IMAGENS}")


if __name__ == "__main__":
  main()
