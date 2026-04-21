# %%

# Importa as bibliotecas necessárias 

import pandas as pd
import sidrapy

data = sidrapy.get_table(table_code="7060", 
                         territorial_level="1", 
                         ibge_territorial_code="all", 
                         variable="63,66",
                         period="last 12",
                         classifications={"315":"all"})
df_raw = data  
df = pd.DataFrame(df_raw)
df

# %%

# Transforma a primeira linha em nome de coluna

df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)
df.columns = df.columns.str.strip()

# Convertendo os tipos das colunas para os dtypes certos

df = df.astype({'Valor':'float', 
                'Mês (Código)':'int',
                'Geral, grupo, subgrupo, item e subitem (Código)':'int',
                'Variável (Código)':'int'
                })

# Mapear manualmente os meses

meses = {
    'janeiro': '01', 'fevereiro': '02', 'março': '03',
    'abril': '04', 'maio': '05', 'junho': '06',
    'julho': '07', 'agosto': '08', 'setembro': '09',
    'outubro': '10', 'novembro': '11', 'dezembro': '12'
}

df['Mês'] = df['Mês'].str.lower().replace(meses, regex=True)
df['Mês'] = pd.to_datetime(df['Mês'], format='%m %Y')

df.rename(columns={
    'Geral, grupo, subgrupo, item e subitem': 'categoria',
    'Valor': 'valor',
    'Mês': 'mes',
    'Variável (Código)': 'variavel_cod'
}, inplace=True)

print(df.dtypes)

# %%

from pathlib import Path
from sqlalchemy import create_engine

print("Criando o Banco de Dados SQLite...")

# Identifica o diretório atual de onde o código está sendo executado
current_dir = Path.cwd()

# Lógica para encontrar o caminho correto dinamicamente:
# Se já estivermos dentro da pasta 'src', salvam direto nela.
# Caso contrário, aponta para a pasta 'src' dentro do diretório atual.
if current_dir.name == 'src':
    db_path = current_dir / 'inflacao_brasil.db'
else:
    db_path = current_dir / 'src' / 'inflacao_brasil.db'

# Garante que a pasta pai do arquivo exista (cria se não existir)
db_path.parent.mkdir(parents=True, exist_ok=True)

# Cria a string de conexão. 
engine = create_engine(f'sqlite:///{db_path}')

# Salva o DataFrame
df.to_sql('fato_ipca', con=engine, if_exists='replace', index=False)

print(f"Dados salvos com sucesso na tabela 'fato_ipca'!\nCaminho: {db_path}")


# %%


