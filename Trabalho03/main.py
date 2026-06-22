import time
import tracemalloc
from pathlib import Path

import algoritmo_guloso
import algoritmo_backtracking
import gerar_imagem


PASTA_IMAGENS = Path(__file__).resolve().parent / "imagens"


REPETICOES_TEMPO = 21


CASOS_DE_TESTE = [
  {
    "nome": "Caso 1 - Grade aberta (guloso acerta o otimo)",
    "descricao": (
      "Sem paredes no caminho: andar sempre em direcao ao destino ja leva\n"
      "  pelo trajeto mais curto. Aqui o guloso encontra a solucao otima."
    ),
    "labirinto": [
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
    ],
  },
  {
    "nome": "Caso 2 - Desvio (guloso acha um caminho, mas nao o menor)",
    "descricao": (
      "O guloso e atraido para perto do destino e entra num desvio longo.\n"
      "  Ele chega ao fim, mas usando mais passos que o caminho otimo."
    ),
    "labirinto": [
      [0, 0, 0, 1, 1, 0, 0],
      [0, 1, 0, 0, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [1, 0, 1, 1, 1, 0, 1],
      [1, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0],
    ],
  },
  {
    "nome": "Caso 3 - Armadilha (guloso falha: fica preso num beco)",
    "descricao": (
      "A heuristica leva o guloso para um beco sem saida. Como ele nao\n"
      "  retrocede, declara 'sem solucao', mesmo existindo um caminho."
    ),
    "labirinto": [
      [0, 1, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1, 0, 0],
      [0, 1, 0, 0, 0, 1, 1],
      [0, 0, 0, 0, 0, 0, 1],
      [0, 0, 1, 1, 0, 1, 0],
      [0, 1, 1, 0, 0, 0, 0],
    ],
  },
  {
    "nome": "Caso 4 - Labirinto grande (custo de tempo, memoria e decisoes)",
    "descricao": (
      "Os dois chegam ao fim, mas o backtracking explora um numero enorme\n"
      "  de possibilidades. Compare tempo, memoria e numero de decisoes."
    ),
    "labirinto": [
      [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
      [1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
      [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
      [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    ],
  },
]


def renderizar(labirinto, caminho=None):
  linhas = len(labirinto)
  colunas = len(labirinto[0])
  inicio = (0, 0)
  objetivo = (linhas - 1, colunas - 1)
  celulas_do_caminho = set(caminho) if caminho else set()

  linhas_texto = []
  for i in range(linhas):
    simbolos = []
    for j in range(colunas):
      if (i, j) == inicio:
        simbolos.append("S")
      elif (i, j) == objetivo:
        simbolos.append("E")
      elif (i, j) in celulas_do_caminho:
        simbolos.append("*")
      elif labirinto[i][j] == 1:
        simbolos.append("#")
      else:
        simbolos.append(".")
    linhas_texto.append("  " + " ".join(simbolos))

  return "\n".join(linhas_texto)


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


def formatar_tempo(segundos):
  return f"{segundos * 1000:.4f} ms"


def formatar_memoria(bytes_):
  if bytes_ < 1024:
    return f"{bytes_} B"
  if bytes_ < 1024 * 1024:
    return f"{bytes_ / 1024:.2f} KB"
  return f"{bytes_ / (1024 * 1024):.2f} MB"


def executar_caso(caso):
  labirinto = caso["labirinto"]

  pico_guloso, (caminho_guloso, decisoes_guloso, percorrido_guloso) = medir_memoria(
    algoritmo_guloso.resolver, labirinto
  )
  tempo_guloso = medir_tempo_medio(algoritmo_guloso.resolver, labirinto)

  pico_bt, (caminho_bt, decisoes_bt, _) = medir_memoria(
    algoritmo_backtracking.resolver, labirinto
  )
  tempo_bt = medir_tempo_medio(algoritmo_backtracking.resolver, labirinto)

  return {
    "nome": caso["nome"],
    "descricao": caso["descricao"],
    "labirinto": labirinto,
    "guloso": {
      "caminho": caminho_guloso,
      "percorrido": percorrido_guloso,
      "passos": contar_passos(caminho_guloso),
      "decisoes": decisoes_guloso,
      "tempo": tempo_guloso,
      "memoria": pico_guloso,
    },
    "backtracking": {
      "caminho": caminho_bt,
      "passos": contar_passos(caminho_bt),
      "decisoes": decisoes_bt,
      "tempo": tempo_bt,
      "memoria": pico_bt,
    },
  }


def texto_resultado(dados):
  if dados["passos"] is None:
    return "Sem solucao"
  return f"Caminho com {dados['passos']} passos"


def texto_melhor_solucao(resultado):
  guloso = resultado["guloso"]
  backtracking = resultado["backtracking"]
  otimo = backtracking["passos"]

  if guloso["passos"] is None:
    coluna_guloso = "Nao encontrou"
  elif guloso["passos"] == otimo:
    coluna_guloso = "Sim (e o otimo)"
  else:
    diferenca = guloso["passos"] - otimo
    coluna_guloso = f"Nao ({diferenca} passos a mais)"

  coluna_bt = f"Sim ({otimo} passos)"
  return coluna_guloso, coluna_bt


def imprimir_tabela(resultado):
  guloso = resultado["guloso"]
  backtracking = resultado["backtracking"]
  melhor_guloso, melhor_bt = texto_melhor_solucao(resultado)

  linhas = [
    ("Resultado obtido", texto_resultado(guloso), texto_resultado(backtracking)),
    ("Melhor solucao encontrada", melhor_guloso, melhor_bt),
    ("Tempo de execucao", formatar_tempo(guloso["tempo"]), formatar_tempo(backtracking["tempo"])),
    ("Numero de decisoes", str(guloso["decisoes"]), str(backtracking["decisoes"])),
    ("Memoria consumida (pico)", formatar_memoria(guloso["memoria"]), formatar_memoria(backtracking["memoria"])),
  ]

  largura_criterio = max(len("Criterio"), *(len(linha[0]) for linha in linhas))
  largura_guloso = max(len("Guloso"), *(len(linha[1]) for linha in linhas))
  largura_bt = max(len("Backtracking"), *(len(linha[2]) for linha in linhas))

  separador = "+-" + "-" * largura_criterio + "-+-" + "-" * largura_guloso + "-+-" + "-" * largura_bt + "-+"

  def formatar_linha(criterio, coluna_guloso, coluna_bt):
    return (
      "| "
      + criterio.ljust(largura_criterio)
      + " | "
      + coluna_guloso.ljust(largura_guloso)
      + " | "
      + coluna_bt.ljust(largura_bt)
      + " |"
    )

  print(separador)
  print(formatar_linha("Criterio", "Guloso", "Backtracking"))
  print(separador)
  for criterio, coluna_guloso, coluna_bt in linhas:
    print(formatar_linha(criterio, coluna_guloso, coluna_bt))
  print(separador)


def imprimir_caso(resultado):
  print("=" * 78)
  print(resultado["nome"])
  print("=" * 78)
  print(resultado["descricao"])
  print()
  print("Labirinto (S=inicio, E=fim, #=parede, .=livre):")
  print(renderizar(resultado["labirinto"]))
  print()

  guloso = resultado["guloso"]
  if guloso["caminho"] is not None:
    print("Caminho do GULOSO (*):")
    print(renderizar(resultado["labirinto"], guloso["caminho"]))
  else:
    preso = guloso["percorrido"][-1]
    print(f"GULOSO ficou preso em {preso} apos {guloso['decisoes']} decisoes (* = trajeto ate travar):")
    print(renderizar(resultado["labirinto"], guloso["percorrido"]))
  print()

  print("Caminho do BACKTRACKING (*):")
  print(renderizar(resultado["labirinto"], resultado["backtracking"]["caminho"]))
  print()

  imprimir_tabela(resultado)
  print()


def imprimir_conclusoes(resultados):
  print("=" * 78)
  print("CONCLUSOES (respostas as perguntas do trabalho)")
  print("=" * 78)
  print()

  print("1) A solucao gulosa e otima ou apenas boa?")
  for resultado in resultados:
    guloso = resultado["guloso"]
    otimo = resultado["backtracking"]["passos"]
    if guloso["passos"] is None:
      situacao = "FALHOU (nao achou caminho, embora exista)"
    elif guloso["passos"] == otimo:
      situacao = f"otima ({guloso['passos']} passos)"
    else:
      situacao = f"apenas boa ({guloso['passos']} passos vs {otimo} do otimo)"
    print(f"   - {resultado['nome'].split(' - ')[0]}: {situacao}")
  print("   => O guloso NAO garante a solucao otima: as vezes acerta, as vezes")
  print("      usa um caminho mais longo e, no pior caso, nem encontra solucao.")
  print()

  print("2) O backtracking encontra a solucao otima?")
  for resultado in resultados:
    backtracking = resultado["backtracking"]
    print(f"   - {resultado['nome'].split(' - ')[0]}: sim, {backtracking['passos']} passos (menor possivel)")
  print("   => Sim. Por explorar todas as alternativas (com poda), ele sempre")
  print("      retorna o caminho mais curto, quando existe um.")
  print()

  print("3) Quanto as solucoes diferem (passos e custo de busca)?")
  for resultado in resultados:
    guloso = resultado["guloso"]
    backtracking = resultado["backtracking"]
    nome_curto = resultado["nome"].split(" - ")[0]
    if guloso["passos"] is None:
      dif_passos = "guloso sem solucao"
    else:
      dif_passos = f"passos {guloso['passos']} x {backtracking['passos']}"
    fator = backtracking["decisoes"] / guloso["decisoes"] if guloso["decisoes"] else 0
    print(
      f"   - {nome_curto}: {dif_passos} | decisoes {guloso['decisoes']} x "
      f"{backtracking['decisoes']} (backtracking explorou {fator:.0f}x mais)"
    )
  print("   => O guloso resolve em tempo e numero de decisoes proporcionais ao")
  print("      tamanho do caminho. O backtracking usa memoria parecida (tambem")
  print("      O(comprimento do caminho), pois a DFS reaproveita a pilha), mas")
  print("      paga MUITO mais em tempo e decisoes para garantir o otimo.")
  print()


def main():
  print()
  print("TRABALHO 03 - CAMINHO EM LABIRINTO")
  print("Comparacao entre algoritmo GULOSO e BACKTRACKING (tentativa e erro)")
  print()

  resultados = []
  for caso in CASOS_DE_TESTE:
    resultado = executar_caso(caso)
    imprimir_caso(resultado)
    resultados.append(resultado)

  imprimir_conclusoes(resultados)

  arquivos = gerar_imagem.gerar_imagens(resultados, PASTA_IMAGENS)
  print("=" * 78)
  print("IMAGENS DO CAMINHO CORRETO")
  print("=" * 78)
  print("Legenda: verde = inicio | vermelho = fim | linha azul = caminho correto")
  print("         (otimo, do backtracking) | laranja = por onde o guloso passou")
  print("         | X vermelho = onde o guloso ficou preso.")
  print()
  for arquivo in arquivos:
    print(f"   - {arquivo}")
  print()


if __name__ == "__main__":
  main()
