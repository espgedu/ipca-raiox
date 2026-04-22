# IPCA Dashboard: Análise de Dados e Visualização com Python

Bem-vindo ao repositório do **IPCA Dashboard**. Este projeto é um painel interativo focado em **Analytics**. O objetivo é pegar os dados brutos da inflação brasileira disponibilizados pelo governo e traduzi-los em visualizações claras, demonstrando na prática como extrair insights do dia a dia utilizando Python.

**[Acesse o Dashboard Interativo Online](https://ipca-analytics.streamlit.app/)**

---

## Foco Analítico
O projeto foi desenhado para responder a perguntas rápidas sobre o cenário macroeconômico sem complicação:
* **A Tendência:** Como a inflação geral se comportou no último ano?
* **Os Vilões:** Quais categorias de produtos e serviços mais encareceram?
* **Pesos Pesados:** Como os gastos essenciais (Alimentação x Transportes) variaram mês a mês?
* **O Retrato Atual:** Uma visão isolada e detalhada de quem puxou o índice no mês mais recente.

---

## Pipeline (ETL)

Para que essa análise simplificada chegasse à tela, foi construído um pipeline de dados simples para garantir a integridade da informação:

1. **Extração:** Conexão direta com a API do Sistema Sidra (IBGE) via biblioteca `sidrapy`, puxando o histórico dinâmico dos últimos 12 meses.
2. **Transformação e Limpeza:**`Pandas` para tratar os dados brutos. Foram aplicadas rotinas de conversão de tipos (datas e floats) e limpeza de strings com Expressões Regulares (`Regex`) para remover os códigos numéricos das categorias do IBGE.
3. **Armazenamento:** Criação de um banco de dados relacional `SQLite` local via `SQLAlchemy`, armazenando a base final limpa (`fato_ipca`) pronta para o consumo da aplicação.
4. **Visualização:** Interface construída inteiramente em `Streamlit` para a web, com gráficos interativos renderizados em `Plotly`, consumindo os dados diretamente via consultas SQL.

## Como executar o projeto localmente

Para testar a extração de dados e visualizar o dashboard na sua máquina, siga os passos:

**1. Clone o repositório:**

git clone [https://https://github.com/espgedu/ipca-raiox](https://github.com/espgedu/ipca-raiox)

cd repo

**2. Instale as dependências:**

pip install -r requirements.txt

**3. Atualize o Banco de Dados**

python src/etl.py

**4. Inicie o Dashboard Web:**

streamlit run viz/app.py

---

Contato e Redes

Eduardo Pinheiro

Profissional de Dados em formação. Focado em transformar dados brutos em informação útil.

[Linkedin](https://linkedin.com/in/edupinheiro)

## Arquitetura do Projeto

A organização dos arquivos foi pensada para separar as responsabilidades de processamento de dados de forma simples.

```text
ipca-raiox/
│
├── src/
│   ├── etl.py                  # Script de extração, tratamento (Pandas) e carga no banco de dados
│   └── inflacao_brasil.db      # Banco de dados SQLite contendo a tabela 'fato_ipca'
│
├── viz/
│   └── app.py                  # Aplicação web principal gerando o dashboard com Streamlit e Plotly
│
├── requirements.txt            # Lista de dependências Python para o deploy
└── README.md                   # Documentação do projeto

---

