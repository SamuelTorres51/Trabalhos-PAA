DIRECOES = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1),
]


def resolver(labirinto):
  linhas = len(labirinto)
  colunas = len(labirinto[0])

  inicio = (0, 0)
  objetivo = (linhas - 1, colunas - 1)

  estado = {
    "decisoes": 0,
    "melhor_caminho": None,
  }

  visitados = [[False] * colunas for _ in range(linhas)]
  caminho_atual = []

  def buscar(linha, coluna):
    estado["decisoes"] += 1

    caminho_atual.append((linha, coluna))
    visitados[linha][coluna] = True

    if (linha, coluna) == objetivo:
      melhor = estado["melhor_caminho"]
      if melhor is None or len(caminho_atual) < len(melhor):
        estado["melhor_caminho"] = list(caminho_atual)
    else:
      for deslocamento_linha, deslocamento_coluna in DIRECOES:
        proxima_linha = linha + deslocamento_linha
        proxima_coluna = coluna + deslocamento_coluna

        dentro_dos_limites = 0 <= proxima_linha < linhas and 0 <= proxima_coluna < colunas
        if not dentro_dos_limites:
          continue

        celula_livre = labirinto[proxima_linha][proxima_coluna] == 0
        ja_visitado = visitados[proxima_linha][proxima_coluna]
        if not celula_livre or ja_visitado:
          continue

        melhor = estado["melhor_caminho"]
        ainda_vale_a_pena = melhor is None or len(caminho_atual) + 1 < len(melhor)
        if ainda_vale_a_pena:
          buscar(proxima_linha, proxima_coluna)

    visitados[linha][coluna] = False
    caminho_atual.pop()

  if labirinto[inicio[0]][inicio[1]] == 0 and labirinto[objetivo[0]][objetivo[1]] == 0:
    buscar(inicio[0], inicio[1])

  return estado["melhor_caminho"], estado["decisoes"], estado["melhor_caminho"]
