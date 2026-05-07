import time
import sys

# ──────────────────────────────────────────────
#  DADOS DO PROBLEMA
# ──────────────────────────────────────────────
valores = [60, 150, 120, 160, 200, 150, 60]
pesos   = [1,   3,   3,   4,   5,   5,  6]
n = len(valores)

# ──────────────────────────────────────────────
#  1. BACKTRACKING (Recursivo)
# ──────────────────────────────────────────────
chamadas_backtracking = 0

def mochila_recursiva(i, W):
    global chamadas_backtracking
    chamadas_backtracking += 1

    if i == 0 or W == 0:
        return 0
    if pesos[i - 1] > W:
        return mochila_recursiva(i - 1, W)

    usar     = valores[i - 1] + mochila_recursiva(i - 1, W - pesos[i - 1])
    nao_usar = mochila_recursiva(i - 1, W)
    return max(usar, nao_usar)

# ──────────────────────────────────────────────
#  2. PROGRAMAÇÃO DINÂMICA
# ──────────────────────────────────────────────
chamadas_pd = 0

def mochila_pd(n, W):
    global chamadas_pd
    chamadas_pd = 0

    # Cria matriz M[n+1][W+1]
    M = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(W + 1):
            chamadas_pd += 1          # conta cada célula preenchida
            if i == 0 or w == 0:
                M[i][w] = 0
            elif pesos[i - 1] <= w:
                M[i][w] = max(
                    valores[i - 1] + M[i - 1][w - pesos[i - 1]],
                    M[i - 1][w]
                )
            else:
                M[i][w] = M[i - 1][w]

    return M[n][W], M

# ──────────────────────────────────────────────
#  RASTREAR ITENS ESCOLHIDOS (PD)
# ──────────────────────────────────────────────
def rastrear_itens(M, n, W):
    itens = []
    w = W
    for i in range(n, 0, -1):
        if M[i][w] != M[i - 1][w]:
            itens.append(i)
            w -= pesos[i - 1]
    itens.reverse()
    return itens

# ──────────────────────────────────────────────
#  IMPRESSÃO DA MATRIZ
# ──────────────────────────────────────────────
def imprimir_matriz(M, n, W):
    header = "     " + "  ".join(f"w={w:2d}" for w in range(W + 1))
    print(header)
    print("-" * len(header))
    for i in range(n + 1):
        linha = f"i={i:2d} | " + "  ".join(f"{M[i][w]:5d}" for w in range(W + 1))
        print(linha)

# ──────────────────────────────────────────────
#  EXECUTAR PARA UM DADO W
# ──────────────────────────────────────────────
def executar(W_teste):
    global chamadas_backtracking

    print("=" * 60)
    print(f"  CAPACIDADE W = {W_teste}")
    print("=" * 60)

    # --- Backtracking ---
    chamadas_backtracking = 0
    sys.setrecursionlimit(100_000)
    t0 = time.perf_counter()
    resultado_bt = mochila_recursiva(n, W_teste)
    t1 = time.perf_counter()
    tempo_bt = (t1 - t0) * 1000   # ms

    print(f"\n[BACKTRACKING RECURSIVO]")
    print(f"  Resultado (valor máximo) : {resultado_bt}")
    print(f"  Tempo de execução        : {tempo_bt:.6f} ms")
    print(f"  Número de chamadas       : {chamadas_backtracking}")

    # --- Programação Dinâmica ---
    chamadas_pd_local = 0
    t2 = time.perf_counter()
    resultado_pd, M = mochila_pd(n, W_teste)
    t3 = time.perf_counter()
    tempo_pd = (t3 - t2) * 1000   # ms
    chamadas_pd_local = chamadas_pd

    itens = rastrear_itens(M, n, W_teste)
    peso_total = sum(pesos[i - 1] for i in itens)
    valor_total = sum(valores[i - 1] for i in itens)

    print(f"\n[PROGRAMAÇÃO DINÂMICA]")
    print(f"  Resultado (valor máximo) : {resultado_pd}")
    print(f"  Tempo de execução        : {tempo_pd:.6f} ms")
    print(f"  Número de células (ops)  : {chamadas_pd_local}")

    print(f"\n  Itens selecionados (índice base 1):")
    for idx in itens:
        print(f"    Item {idx}: peso={pesos[idx-1]}, valor={valores[idx-1]}")
    print(f"  Peso total usado: {peso_total} / {W_teste}")
    print(f"  Valor total     : {valor_total}")

    print(f"\n  Matriz de Programação Dinâmica M[i][w]:")
    imprimir_matriz(M, n, W_teste)

    print(f"\n{'─'*60}")
    print(f"  TABELA RESUMO  (W = {W_teste})")
    print(f"{'─'*60}")
    print(f"  {'Critério':<30} {'Backtracking':>12} {'Dinâmico':>12}")
    print(f"  {'─'*54}")
    print(f"  {'Resultado':.<30} {resultado_bt:>12} {resultado_pd:>12}")
    print(f"  {'Tempo (ms)':.<30} {tempo_bt:>12.6f} {tempo_pd:>12.6f}")
    print(f"  {'Nº de chamadas/operações':.<30} {chamadas_backtracking:>12} {chamadas_pd_local:>12}")
    print()

# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("\nPROBLEMA DA MOCHILA — Trabalho 02")
    print(f"Itens: n={n}")
    print(f"Valores: {valores}")
    print(f"Pesos  : {pesos}\n")

    executar(6)
    executar(10)