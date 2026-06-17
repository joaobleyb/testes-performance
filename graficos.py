from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_RESULTADOS = PASTA_PROJETO / "resultados"

arquivos = {
    10: PASTA_RESULTADOS / "resultados_10_stats.csv",
    50: PASTA_RESULTADOS / "resultados_50_stats.csv",
    100: PASTA_RESULTADOS / "resultados_100_stats.csv",
}

usuarios = []
throughput = []
p50 = []
p90 = []
p95 = []
p99 = []
requisicoes = []
falhas = []
taxa_erros = []


for quantidade_usuarios, arquivo in arquivos.items():
    if not arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    df = pd.read_csv(arquivo)

    linha_total = df[df["Name"] == "Aggregated"]

    if linha_total.empty:
        linha_total = df.tail(1)

    total = linha_total.iloc[0]

    total_requisicoes = int(total["Request Count"])
    total_falhas = int(total["Failure Count"])

    if total_requisicoes > 0:
        percentual_erros = (
            total_falhas / total_requisicoes
        ) * 100
    else:
        percentual_erros = 0

    usuarios.append(quantidade_usuarios)
    throughput.append(float(total["Requests/s"]))
    p50.append(float(total["50%"]))
    p90.append(float(total["90%"]))
    p95.append(float(total["95%"]))
    p99.append(float(total["99%"]))
    requisicoes.append(total_requisicoes)
    falhas.append(total_falhas)
    taxa_erros.append(percentual_erros)


def adicionar_valores(x, y, casas=1, sufixo=""):
    for valor_x, valor_y in zip(x, y):
        plt.annotate(
            f"{valor_y:.{casas}f}{sufixo}",
            (valor_x, valor_y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
        )


# GRÁFICO 1 — THROUGHPUT
plt.figure(figsize=(9, 5))

plt.plot(
    usuarios,
    throughput,
    marker="o",
    linewidth=2,
    label="Throughput",
)

adicionar_valores(
    usuarios,
    throughput,
    casas=2,
    sufixo=" req/s",
)

plt.title("Throughput por quantidade de usuários")
plt.xlabel("Usuários simultâneos")
plt.ylabel("Requisições por segundo")
plt.xticks(usuarios)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    PASTA_RESULTADOS / "grafico_throughput.png",
    dpi=300,
)

plt.show()


# GRÁFICO 2 — PERCENTIS
plt.figure(figsize=(9, 5))

plt.plot(usuarios, p50, marker="o", label="p50")
plt.plot(usuarios, p90, marker="o", label="p90")
plt.plot(usuarios, p95, marker="o", label="p95")
plt.plot(usuarios, p99, marker="o", label="p99")

for valores in [p50, p90, p95, p99]:
    adicionar_valores(
        usuarios,
        valores,
        casas=0,
        sufixo=" ms",
    )

plt.title("Percentis do tempo de resposta")
plt.xlabel("Usuários simultâneos")
plt.ylabel("Tempo de resposta em milissegundos")
plt.xticks(usuarios)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    PASTA_RESULTADOS / "grafico_percentis.png",
    dpi=300,
)

plt.show()


# GRÁFICO 3 — REQUISIÇÕES, FALHAS E TAXA DE ERRO

fig, eixo1 = plt.subplots(figsize=(10, 6))

largura = 0.32
posicoes = list(range(len(usuarios)))

posicoes_requisicoes = [
    posicao - largura / 2
    for posicao in posicoes
]

posicoes_falhas = [
    posicao + largura / 2
    for posicao in posicoes
]

# Barras de requisições
barras_requisicoes = eixo1.bar(
    posicoes_requisicoes,
    requisicoes,
    width=largura,
    label="Requisições",
)

# Barras de falhas
barras_falhas = eixo1.bar(
    posicoes_falhas,
    falhas,
    width=largura,
    label="Falhas",
)

eixo1.set_title("Requisições, falhas e taxa de erro")
eixo1.set_xlabel("Usuários simultâneos")
eixo1.set_ylabel("Quantidade")
eixo1.set_xticks(posicoes)
eixo1.set_xticklabels(usuarios)
eixo1.grid(axis="y", linestyle="--", alpha=0.5)

# Valores em cima das barras
for barra in barras_requisicoes:
    altura = barra.get_height()

    eixo1.annotate(
        f"{int(altura)}",
        xy=(
            barra.get_x() + barra.get_width() / 2,
            altura,
        ),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

for barra in barras_falhas:
    altura = barra.get_height()

    eixo1.annotate(
        f"{int(altura)}",
        xy=(
            barra.get_x() + barra.get_width() / 2,
            altura,
        ),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

# Segundo eixo para a taxa de erro
eixo2 = eixo1.twinx()

# Apenas pontos, sem linha ligando
pontos_taxa = eixo2.scatter(
    posicoes,
    taxa_erros,
    marker="D",
    s=70,
    label="Taxa de erro",
    zorder=5,
)

eixo2.set_ylabel("Taxa de erro (%)")

# Deixa uma margem no eixo para os textos
maior_taxa = max(taxa_erros)

if maior_taxa == 0:
    eixo2.set_ylim(0, 1)
else:
    eixo2.set_ylim(0, maior_taxa * 1.4)

# Valores da taxa de erro
for posicao, valor in zip(posicoes, taxa_erros):
    eixo2.annotate(
        f"{valor:.2f}%",
        xy=(posicao, valor),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

# Juntar as legendas dos dois eixos
elementos1, rotulos1 = eixo1.get_legend_handles_labels()
elementos2, rotulos2 = eixo2.get_legend_handles_labels()

eixo1.legend(
    elementos1 + elementos2,
    rotulos1 + rotulos2,
    loc="upper left",
)

fig.tight_layout()

plt.savefig(
    PASTA_RESULTADOS
    / "grafico_requisicoes_falhas_erros.png",
    dpi=300,
)

plt.show()