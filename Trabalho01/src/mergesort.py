def _intercalar(esquerda, direita):
    resultado = []
    indice_esquerda = 0
    indice_direita = 0

    while indice_esquerda < len(esquerda) and indice_direita < len(direita):
        if esquerda[indice_esquerda] <= direita[indice_direita]:
            resultado.append(esquerda[indice_esquerda])
            indice_esquerda += 1
        else:
            resultado.append(direita[indice_direita])
            indice_direita += 1

    resultado.extend(esquerda[indice_esquerda:])
    resultado.extend(direita[indice_direita:])
    return resultado


def mergesort(arr):
    if len(arr) <= 1:
        return arr[:]

    meio = len(arr) // 2
    metade_esquerda = mergesort(arr[:meio])
    metade_direita = mergesort(arr[meio:])
    return _intercalar(metade_esquerda, metade_direita)
