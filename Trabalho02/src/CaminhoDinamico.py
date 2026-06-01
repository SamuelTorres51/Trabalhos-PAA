def caminho_minimo_dinamico(matriz):
  total_linhas = len(matriz)
  total_colunas = len(matriz[0])

  dp = [[0 for _ in range(total_colunas)] for _ in range(total_linhas)]

  dp[0][0] = matriz[0][0]

  for i in range(1, total_linhas):
    dp[i][0] = dp[i - 1][0] + matriz[i][0]

  for j in range(1, total_colunas):
    dp[0][j] = dp[0][j - 1] + matriz[0][j]

  for i in range(1, total_linhas):
    for j in range(1, total_colunas):
      dp[i][j] = matriz[i][j] + min(
        dp[i - 1][j],
        dp[i][j - 1]
      )

  return dp[total_linhas - 1][total_colunas - 1]


if __name__ == "__main__":
  matriz = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
  ]

  resultado = caminho_minimo_dinamico(matriz)

  print("Menor caminho:", resultado)
