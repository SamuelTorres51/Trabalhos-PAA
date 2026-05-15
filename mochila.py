import time
import sys
import random

sys.setrecursionlimit(10_000_000)
random.seed(42)

# ──────────────────────────────────────────────
#  GERANDO 50 ITENS ALEATORIOS
# ──────────────────────────────────────────────
n = 50
valores = [random.randint(10, 300) for _ in range(n)]
pesos   = [random.randint(1,  15)  for _ in range(n)]
W = 50

print("----- RESUMO DO PROBLEMA-------")
print("PROBLEMA DA MOCHILA -- 50 itens")
print(f"Valores: {valores}")
print(f"Pesos  : {pesos}")
print(f"Capacidade W = {W}\n")

# ──────────────────────────────────────────────
#  1. BACKTRACKING PURO
# ──────────────────────────────────────────────
chamadas_bt = 0

def mochila_recursiva(i, W):
    global chamadas_bt
    chamadas_bt += 1
    if i == 0 or W == 0:
        return 0
    if pesos[i - 1] > W:
        return mochila_recursiva(i - 1, W)
    usar     = valores[i - 1] + mochila_recursiva(i - 1, W - pesos[i - 1])
    nao_usar = mochila_recursiva(i - 1, W)
    return max(usar, nao_usar)

# ──────────────────────────────────────────────
#  2. PROGRAMACAO DINAMICA
# ──────────────────────────────────────────────
chamadas_pd = 0

def mochila_pd(n, W):
    global chamadas_pd
    chamadas_pd = 0
    M = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for w in range(W + 1):
            chamadas_pd += 1
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
#  BACKTRACKING
# ──────────────────────────────────────────────
print("[BACKTRACKING RECURSIVO] -- iniciando...")
t0 = time.perf_counter()
resultado_bt = mochila_recursiva(n, W)
tempo_bt = (time.perf_counter() - t0) * 1000

print(f"  Resultado      : {resultado_bt}")
print(f"  Tempo          : {tempo_bt:.4f} ms")
print(f"  No de chamadas : {chamadas_bt}\n")

# ──────────────────────────────────────────────
#  PROGRAMACAO DINAMICA
# ──────────────────────────────────────────────
print("[PROGRAMACAO DINAMICA] -- iniciando...")
t1 = time.perf_counter()
resultado_pd, M = mochila_pd(n, W)
tempo_pd = (time.perf_counter() - t1) * 1000

print(f"  Resultado      : {resultado_pd}")
print(f"  Tempo          : {tempo_pd:.4f} ms")
print(f"  No de celulas  : {chamadas_pd}\n")

# ──────────────────────────────────────────────
#  TABELA RESUMO
# ──────────────────────────────────────────────
print("=" * 55)
print(f"  TABELA RESUMO  (n=50, W={W})")
print("=" * 55)
print(f"  {'Criterio':<28} {'Backtracking':>12} {'Dinamico':>12}")
print(f"  {'-'*52}")
print(f"  {'Resultado':.<28} {resultado_bt:>12} {resultado_pd:>12}")
print(f"  {'Tempo (ms)':.<28} {tempo_bt:>12.4f} {tempo_pd:>12.4f}")
print(f"  {'No chamadas/operacoes':.<28} {chamadas_bt:>12} {chamadas_pd:>12}")