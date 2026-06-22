from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


COR_PAREDE = (0.18, 0.20, 0.25)
COR_LIVRE = (0.93, 0.94, 0.96)
COR_RASTRO_GULOSO = (1.00, 0.80, 0.60)
COR_INICIO = (0.30, 0.69, 0.31)
COR_FIM = (0.90, 0.22, 0.21)
COR_CAMINHO_CORRETO = (0.13, 0.59, 0.95)
COR_GRADE = (0.78, 0.80, 0.84)


def construir_imagem_base(labirinto, rastro_guloso):
  linhas = len(labirinto)
  colunas = len(labirinto[0])
  imagem = np.zeros((linhas, colunas, 3))

  for i in range(linhas):
    for j in range(colunas):
      imagem[i, j] = COR_PAREDE if labirinto[i][j] == 1 else COR_LIVRE

  for i, j in rastro_guloso or []:
    if labirinto[i][j] == 0:
      imagem[i, j] = COR_RASTRO_GULOSO

  imagem[0, 0] = COR_INICIO
  imagem[linhas - 1, colunas - 1] = COR_FIM

  return imagem


def texto_metricas(resultado):
  guloso = resultado["guloso"]
  backtracking = resultado["backtracking"]

  if guloso["caminho"] is None:
    parte_guloso = "Guloso: sem solucao"
  else:
    parte_guloso = f"Guloso: {guloso['passos']} passos"

  parte_bt = f"Otimo (backtracking): {backtracking['passos']} passos"
  parte_decisoes = f"decisoes {guloso['decisoes']} x {backtracking['decisoes']}"

  return f"{parte_guloso}  |  {parte_bt}  |  {parte_decisoes}"


def desenhar_caso(eixo, resultado):
  labirinto = resultado["labirinto"]
  linhas = len(labirinto)
  colunas = len(labirinto[0])

  guloso = resultado["guloso"]
  backtracking = resultado["backtracking"]
  guloso_falhou = guloso["caminho"] is None
  rastro_guloso = guloso["caminho"] if not guloso_falhou else guloso["percorrido"]

  imagem = construir_imagem_base(labirinto, rastro_guloso)
  eixo.imshow(imagem, origin="upper", extent=(-0.5, colunas - 0.5, linhas - 0.5, -0.5))

  eixo.set_xticks(np.arange(-0.5, colunas, 1))
  eixo.set_yticks(np.arange(-0.5, linhas, 1))
  eixo.grid(color=COR_GRADE, linewidth=1)
  eixo.tick_params(length=0, labelbottom=False, labelleft=False)

  caminho_correto = backtracking["caminho"]
  if caminho_correto:
    coordenadas_x = [coluna for _, coluna in caminho_correto]
    coordenadas_y = [linha for linha, _ in caminho_correto]
    eixo.plot(
      coordenadas_x,
      coordenadas_y,
      color=COR_CAMINHO_CORRETO,
      linewidth=4,
      solid_capstyle="round",
      solid_joinstyle="round",
      zorder=3,
    )

  if guloso_falhou and rastro_guloso:
    linha_presa, coluna_presa = rastro_guloso[-1]
    eixo.plot(
      coluna_presa,
      linha_presa,
      marker="X",
      color=COR_FIM,
      markersize=15,
      markeredgecolor="white",
      markeredgewidth=1.5,
      zorder=4,
    )

  eixo.set_title(texto_metricas(resultado), fontsize=10)


def construir_legenda(houve_falha):
  itens = [
    Line2D([0], [0], color=COR_CAMINHO_CORRETO, linewidth=4, label="Caminho correto (otimo)"),
    Patch(facecolor=COR_RASTRO_GULOSO, edgecolor=COR_GRADE, label="Rastro do guloso"),
    Patch(facecolor=COR_INICIO, edgecolor=COR_GRADE, label="Inicio"),
    Patch(facecolor=COR_FIM, edgecolor=COR_GRADE, label="Fim"),
  ]
  if houve_falha:
    itens.append(
      Line2D(
        [0],
        [0],
        marker="X",
        color="none",
        markerfacecolor=COR_FIM,
        markeredgecolor="white",
        markersize=11,
        label="Guloso travou",
      )
    )
  return itens


def gerar_imagens(resultados, pasta_saida):
  pasta = Path(pasta_saida)
  pasta.mkdir(parents=True, exist_ok=True)

  arquivos_gerados = []
  for indice, resultado in enumerate(resultados, start=1):
    labirinto = resultado["labirinto"]
    linhas = len(labirinto)
    colunas = len(labirinto[0])
    guloso_falhou = resultado["guloso"]["caminho"] is None

    figura, eixo = plt.subplots(figsize=(colunas * 0.55 + 1.5, linhas * 0.55 + 2.2))
    figura.suptitle(resultado["nome"], fontsize=12, fontweight="bold")

    desenhar_caso(eixo, resultado)
    eixo.set_aspect("equal")

    eixo.legend(
      handles=construir_legenda(guloso_falhou),
      loc="upper center",
      bbox_to_anchor=(0.5, -0.02),
      ncol=2,
      frameon=False,
      fontsize=9,
    )

    caminho_arquivo = pasta / f"caso_{indice}.png"
    figura.savefig(caminho_arquivo, dpi=130, bbox_inches="tight")
    plt.close(figura)

    arquivos_gerados.append(caminho_arquivo)

  return arquivos_gerados
