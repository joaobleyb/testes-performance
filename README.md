# Testes de Performance com Locust

Testes de performance na API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com) utilizando o Locust. Os testes simulam usuários acessando endpoints de consulta e criação de dados, sendo executados em modo headless com resultados exportados para CSV.

---

## Cenários testados

| Cenário                | Método | Endpoint       | Peso |
|------------------------|--------|----------------|------|
| Listar posts           | GET    | `/posts`       | 4    |
| Buscar post específico | GET    | `/posts/{id}`  | 3    |
| Listar comentários     | GET    | `/comments`    | 2    |
| Criar post             | POST   | `/posts`       | 2    |
| Criar comentário       | POST   | `/comments`    | 1    |

> Os pesos fazem com que as consultas sejam executadas com maior frequência do que as operações de criação, representando um uso mais próximo do real.

---

## Estrutura do projeto

```
testes-performance/
├── .gitignore
├── locustfile.py
├── graficos.py
├── executar_testes.bat
├── README.md
└── resultados/
```

---

## Requisitos

**Python** — versão utilizada no desenvolvimento: `3.14.5`

Instale as dependências necessárias:

```bash
# Locust (obrigatório)
pip install locust

# Geração de gráficos (opcional)
pip install pandas matplotlib
```

Para verificar se o Locust foi instalado corretamente:

```bash
locust --version
```

---

## Execução dos testes

Antes de executar, confirme que o terminal está aberto na pasta do projeto:

```powershell
cd S:\testes-performance
```

### Executar em modo headless

**10 usuários**

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 1m
```

**50 usuários**

```bash
locust -f locustfile.py --headless -u 50 -r 5 -t 1m
```

**100 usuários**

```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 1m
```

### Exportar resultados para CSV

Antes de executar, confirme que existe uma pasta chamada `resultados`.

**10 usuários**

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 1m --csv resultados/resultados_10
```

**50 usuários**

```bash
locust -f locustfile.py --headless -u 50 -r 5 -t 1m --csv resultados/resultados_50
```

**100 usuários**

```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 1m --csv resultados/resultados_100
```

### Executar os três testes em sequência

No terminal do VS Code:

```powershell
locust -f locustfile.py --headless -u 10 -r 2 -t 1m --csv resultados/resultados_10; locust -f locustfile.py --headless -u 50 -r 5 -t 1m --csv resultados/resultados_50; locust -f locustfile.py --headless -u 100 -r 10 -t 1m --csv resultados/resultados_100
```

Os três testes serão executados em sequência, começando pelo teste com 10 usuários, depois 50 usuários e, por último, 100 usuários.

---

## Arquivos gerados

Após as execuções, a pasta `resultados/` conterá:

```
resultados/
├── resultados_10_stats.csv
├── resultados_10_stats_history.csv
├── resultados_10_failures.csv
├── resultados_50_stats.csv
├── resultados_50_stats_history.csv
├── resultados_50_failures.csv
├── resultados_100_stats.csv
├── resultados_100_stats_history.csv
└── resultados_100_failures.csv
```

Os arquivos `*_stats.csv` são os principais para análise e contêm:

- Quantidade de requisições e falhas
- Tempo médio de resposta
- Percentis p90 e p95
- Requisições por segundo

---

## Geração dos gráficos

Após executar os três testes, execute:

```bash
python graficos.py
```

O script lê os CSVs da pasta `resultados/` e gera:

| Arquivo                          | Conteúdo                                           |
|----------------------------------|----------------------------------------------------|
| `resultados/grafico_throughput.png` | Comparação de requisições por segundo entre as cargas |
| `resultados/grafico_percentis.png`  | Tempos de resposta p90 e p95 para 10, 50 e 100 usuários |

---

## Referência dos parâmetros

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 1m --csv resultados/resultados_10
```

| Parâmetro          | Descrição                              |
|--------------------|----------------------------------------|
| `-f locustfile.py` | Arquivo de teste                       |
| `--headless`       | Executa sem abrir a interface web      |
| `-u 10`            | Número de usuários simultâneos         |
| `-r 2`             | Usuários adicionados por segundo       |
| `-t 1m`            | Duração do teste                       |
| `--csv`            | Exporta os resultados para arquivos CSV |

---

## Observações

A API JSONPlaceholder é externa e pública. Os resultados podem ser influenciados pela conexão com a internet, localização do servidor ou limitações do próprio serviço.

---

## Autor

João Vitor Bley Bier