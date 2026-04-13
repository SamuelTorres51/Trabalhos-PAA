# Analise Assintotica

## Mergesort

- Melhor caso: O(n log n)
- Caso medio: O(n log n)
- Pior caso: O(n log n)

O algoritmo divide o vetor ao meio recursivamente e depois faz a intercalação das partes ordenadas. A divisao ocorre log n vezes e, em cada nivel, todo o vetor e processado uma vez, resultando em O(n log n).

## TimSort

- Melhor caso: O(n log n)
- Caso medio: O(n log n)
- Pior caso: O(n log n)

Nesta implementacao, o vetor e dividido em blocos ordenados com insertion sort e depois os blocos sao mesclados. A complexidade final permanece O(n log n), com melhor aproveitamento em entradas parcialmente ordenadas quando comparado ao Mergesort.

## Comparacao

Os dois algoritmos apresentam classe de complexidade O(n log n). Na pratica, o TimSort tende a se comportar melhor em entradas que ja possuem ordem parcial, enquanto o Mergesort apresenta comportamento mais uniforme.
