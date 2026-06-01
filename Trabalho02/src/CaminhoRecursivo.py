def caminho_minimo_recursivo(matriz, linha=0, coluna=0):
  total_linhas = len(matriz)
  total_colunas = len(matriz[0])

  if linha == total_linhas - 1 and coluna == total_colunas - 1:
    return matriz[linha][coluna]

  if linha >= total_linhas or coluna >= total_colunas:
    return float('inf')

  baixo = caminho_minimo_recursivo(matriz, linha + 1, coluna)

  direita = caminho_minimo_recursivo(matriz, linha, coluna + 1)

  return matriz[linha][coluna] + min(baixo, direita)


if __name__ == "__main__":
  matriz = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
  ]

  resultado = caminho_minimo_recursivo(matriz)

  print("Menor caminho:", resultado)
