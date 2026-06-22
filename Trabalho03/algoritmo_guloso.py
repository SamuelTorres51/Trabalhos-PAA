DIRECOES = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1),
]


def distancia_manhattan(origem, destino):
  return abs(origem[0] - destino[0]) + abs(origem[1] - destino[1])


def vizinhos_validos(labirinto, atual, visitados):
  linhas = len(labirinto)
  colunas = len(labirinto[0])
  candidatos = []

  for deslocamento_linha, deslocamento_coluna in DIRECOES:
    proxima_linha = atual[0] + deslocamento_linha
    proxima_coluna = atual[1] + deslocamento_coluna

    dentro_dos_limites = 0 <= proxima_linha < linhas and 0 <= proxima_coluna < colunas
    if not dentro_dos_limites:
      continue

    celula_livre = labirinto[proxima_linha][proxima_coluna] == 0
    ja_visitado = (proxima_linha, proxima_coluna) in visitados

    if celula_livre and not ja_visitado:
      candidatos.append((proxima_linha, proxima_coluna))

  return candidatos


def resolver(labirinto):
  linhas = len(labirinto)
  colunas = len(labirinto[0])

  inicio = (0, 0)
  objetivo = (linhas - 1, colunas - 1)

  if labirinto[inicio[0]][inicio[1]] == 1 or labirinto[objetivo[0]][objetivo[1]] == 1:
    return None, 0, [inicio]

  atual = inicio
  visitados = {inicio}
  caminho_percorrido = [inicio]
  decisoes = 0

  while atual != objetivo:
    decisoes += 1

    candidatos = vizinhos_validos(labirinto, atual, visitados)

    if not candidatos:
      return None, decisoes, caminho_percorrido

    proximo = min(candidatos, key=lambda celula: distancia_manhattan(celula, objetivo))

    visitados.add(proximo)
    caminho_percorrido.append(proximo)
    atual = proximo

  return caminho_percorrido, decisoes, caminho_percorrido
