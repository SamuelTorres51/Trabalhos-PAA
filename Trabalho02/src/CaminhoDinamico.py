# algoritmo_dinamico.py

def caminho_minimo_dinamico(matriz):
    """
    Calcula o menor custo para sair da posição (0,0)
    até a posição final da matriz utilizando
    Programação Dinâmica (tabulação).

    Movimentos permitidos:
    - Direita
    - Baixo
    """

    total_linhas = len(matriz)
    total_colunas = len(matriz[0])

    # Cria a matriz DP
    dp = [[0 for _ in range(total_colunas)] for _ in range(total_linhas)]

    # Posição inicial
    dp[0][0] = matriz[0][0]

    # Preenche a primeira coluna
    for i in range(1, total_linhas):
        dp[i][0] = dp[i - 1][0] + matriz[i][0]

    # Preenche a primeira linha
    for j in range(1, total_colunas):
        dp[0][j] = dp[0][j - 1] + matriz[0][j]

    # Preenche o restante da matriz
    for i in range(1, total_linhas):
        for j in range(1, total_colunas):

            dp[i][j] = matriz[i][j] + min(
                dp[i - 1][j],     # vindo de cima
                dp[i][j - 1]      # vindo da esquerda
            )

    # Retorna o valor do canto inferior direito
    return dp[total_linhas - 1][total_colunas - 1]


# Exemplo de teste
if __name__ == "__main__":

    matriz = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]

    resultado = caminho_minimo_dinamico(matriz)

    print("Menor caminho:", resultado)