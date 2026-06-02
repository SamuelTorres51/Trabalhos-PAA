def caminho_minimo_recursivo(matriz, linha=0, coluna=0):
  total_linhas = len(matriz)
  total_colunas = len(matriz[0])

  if linha == total_linhas - 1 and coluna == total_colunas - 1:
    return matriz[linha][coluna], [(linha, coluna)]

  if linha >= total_linhas or coluna >= total_colunas:
    return float('inf'), []

  custo_baixo, caminho_baixo = caminho_minimo_recursivo(matriz, linha + 1, coluna)
  custo_direita, caminho_direita = caminho_minimo_recursivo(matriz, linha, coluna + 1)

  if custo_baixo <= custo_direita:
    return matriz[linha][coluna] + custo_baixo, [(linha, coluna)] + caminho_baixo
  else:
    return matriz[linha][coluna] + custo_direita, [(linha, coluna)] + caminho_direita


if __name__ == "__main__":
  matriz = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
  ]

  custo, caminho = caminho_minimo_recursivo(matriz)

  print("Menor custo:", custo)
  print("Caminho:", " -> ".join(str(p) for p in caminho))
