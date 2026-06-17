from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PASTA_ATUAL = Path(__file__).resolve().parent
PASTA_RESULTADOS = PASTA_ATUAL / "resultados"

arquivos = {
    "10 usuários": PASTA_RESULTADOS / "resultados_10_stats.csv",
    "50 usuários": PASTA_RESULTADOS / "resultados_50_stats.csv",
    "100 usuários": PASTA_RESULTADOS / "resultados_100_stats.csv",
}

usuarios = []
throughput = []
p90 = []
p95 = []

for nome, arquivo in arquivos.items():
    if not arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    df = pd.read_csv(arquivo)

    total = df[df["Name"] == "Aggregated"]

    if total.empty:
        raise ValueError(
            f"A linha Aggregated não foi encontrada em {arquivo.name}"
        )

    total = total.iloc[0]

    usuarios.append(nome)
    throughput.append(total["Requests/s"])
    p90.append(total["90%"])
    p95.append(total["95%"])

plt.figure()
plt.plot(usuarios, throughput, marker="o")
plt.title("Throughput por quantidade de usuários")
plt.xlabel("Carga")
plt.ylabel("Requisições por segundo")
plt.grid(True)
plt.tight_layout()
plt.savefig(PASTA_RESULTADOS / "grafico_throughput.png")
plt.show()

plt.figure()
plt.plot(usuarios, p90, marker="o", label="p90")
plt.plot(usuarios, p95, marker="o", label="p95")
plt.title("Percentis de tempo de resposta")
plt.xlabel("Carga")
plt.ylabel("Tempo de resposta em ms")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(PASTA_RESULTADOS / "grafico_percentis.png")
plt.show()