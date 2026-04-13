def _calcular_minrun(tamanho):
    resto = 0
    while tamanho >= 64:
        resto |= tamanho & 1
        tamanho >>= 1
    return tamanho + resto


def _insertion_sort_intervalo(vetor, inicio, fim):
    for i in range(inicio + 1, fim):
        valor_atual = vetor[i]
        j = i - 1
        while j >= inicio and vetor[j] > valor_atual:
            vetor[j + 1] = vetor[j]
            j -= 1
        vetor[j + 1] = valor_atual


def _mesclar(vetor, inicio, meio, fim):
    esquerda = vetor[inicio:meio]
    direita = vetor[meio:fim]

    indice_esquerda = 0
    indice_direita = 0
    indice_saida = inicio

    while indice_esquerda < len(esquerda) and indice_direita < len(direita):
        if esquerda[indice_esquerda] <= direita[indice_direita]:
            vetor[indice_saida] = esquerda[indice_esquerda]
            indice_esquerda += 1
        else:
            vetor[indice_saida] = direita[indice_direita]
            indice_direita += 1
        indice_saida += 1

    while indice_esquerda < len(esquerda):
        vetor[indice_saida] = esquerda[indice_esquerda]
        indice_esquerda += 1
        indice_saida += 1

    while indice_direita < len(direita):
        vetor[indice_saida] = direita[indice_direita]
        indice_direita += 1
        indice_saida += 1


def _mesclar_runs(vetor, pilha_runs, indice):
    inicio_esquerda, tamanho_esquerda = pilha_runs[indice]
    inicio_direita, tamanho_direita = pilha_runs[indice + 1]

    _mesclar(vetor, inicio_esquerda, inicio_direita, inicio_direita + tamanho_direita)

    pilha_runs[indice] = (inicio_esquerda, tamanho_esquerda + tamanho_direita)
    del pilha_runs[indice + 1]


def timsort(arr):
    tamanho = len(arr)
    if tamanho <= 1:
        return arr[:]

    vetor = arr[:]
    minrun = _calcular_minrun(tamanho)
    pilha_runs = []

    inicio = 0
    while inicio < tamanho:
        fim = min(inicio + minrun, tamanho)
        _insertion_sort_intervalo(vetor, inicio, fim)
        pilha_runs.append((inicio, fim - inicio))

        while len(pilha_runs) > 1:
            n = len(pilha_runs)
            condicao_a = n >= 3 and pilha_runs[n - 3][1] <= pilha_runs[n - 2][1] + pilha_runs[n - 1][1]
            condicao_b = pilha_runs[n - 2][1] <= pilha_runs[n - 1][1]

            if not (condicao_a or condicao_b):
                break

            if condicao_a and pilha_runs[n - 3][1] < pilha_runs[n - 1][1]:
                _mesclar_runs(vetor, pilha_runs, n - 3)
            else:
                _mesclar_runs(vetor, pilha_runs, n - 2)

        inicio = fim

    while len(pilha_runs) > 1:
        _mesclar_runs(vetor, pilha_runs, len(pilha_runs) - 2)

    return vetor
