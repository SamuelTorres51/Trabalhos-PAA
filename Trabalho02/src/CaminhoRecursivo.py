# algoritmo_recursivo.py

def caminho_minimo_recursivo(matriz, linha=0, coluna=0):
    """
    Calcula o menor custo para sair da posição (0,0)
    até a posição final da matriz utilizando recursão pura.

    Movimentos permitidos:
    - Direita
    - Baixo
    """

    total_linhas = len(matriz)
    total_colunas = len(matriz[0])

    # Caso base:
    # chegou no canto inferior direito
    if linha == total_linhas - 1 and coluna == total_colunas - 1:
        return matriz[linha][coluna]

    # Caso esteja fora da matriz
    if linha >= total_linhas or coluna >= total_colunas:
        return float('inf')

    # Caminho indo para baixo
    baixo = caminho_minimo_recursivo(matriz, linha + 1, coluna)

    # Caminho indo para direita
    direita = caminho_minimo_recursivo(matriz, linha, coluna + 1)

    # Retorna o menor caminho possível
    return matriz[linha][coluna] + min(baixo, direita)


# Exemplo de teste
if __name__ == "__main__":

    matriz = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]

    resultado = caminho_minimo_recursivo(matriz)

    print("Menor caminho:", resultado)