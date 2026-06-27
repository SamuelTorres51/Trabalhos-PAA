import random
from collections import deque


DIRECOES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def _tem_caminho(labirinto):
  n = len(labirinto)
  if labirinto[0][0] == 1 or labirinto[n - 1][n - 1] == 1:
    return False

  visitados = [[False] * n for _ in range(n)]
  fila = deque([(0, 0)])
  visitados[0][0] = True

  while fila:
    linha, coluna = fila.popleft()
    if (linha, coluna) == (n - 1, n - 1):
      return True
    for dl, dc in DIRECOES:
      nl, nc = linha + dl, coluna + dc
      if 0 <= nl < n and 0 <= nc < n and not visitados[nl][nc] and labirinto[nl][nc] == 0:
        visitados[nl][nc] = True
        fila.append((nl, nc))

  return False


def gerar_labirinto(tamanho, semente, densidade_paredes=0.28):
  """Gera um labirinto quadrado (tamanho x tamanho) com solucao garantida.

  Usa uma semente fixa para que o mesmo labirinto seja reproduzido a cada
  execucao (util para a demonstracao em aula). Sorteia paredes ate obter um
  labirinto em que exista caminho do inicio (0, 0) ao fim (tamanho-1, tamanho-1).
  """
  rng = random.Random(semente)

  while True:
    labirinto = [
      [1 if rng.random() < densidade_paredes else 0 for _ in range(tamanho)]
      for _ in range(tamanho)
    ]
    labirinto[0][0] = 0
    labirinto[tamanho - 1][tamanho - 1] = 0

    if _tem_caminho(labirinto):
      return labirinto
