import mysql.connector
import pandas as pd
import streamlit as st
#Conectar ao banco de dados
connection = mysql.connector.connect(
    host='roundhouse.proxy.rlwy.net',
    user='root',
    password='-gceg36h5FB1ggBDFC6Bgaa51hcbh53D',
    port=35304,
    database='railway'
)
# Função para executar consultas e obter resultados em um DataFrame
def execute_query(query):
    return pd.read_sql_query(query, connection)

# Título do aplicativo
st.title("Análise OLAP - Data Warehouse")

st.title('Pergunta 4')

st.subheader('Qual é o valor total pago por modalidade de licitação e fonte de recursos, considerando um ano específico?')

# Adicione menus suspensos para selecionar a modalidade de licitação, a fonte de recursos e o ano
modalidades = execute_query("SELECT DISTINCT nome FROM dim_modalidade_licitacao ORDER BY nome;")
modalidade_selecionada = st.selectbox("Selecione a modalidade de licitação:", ["Todas as Modalidades"] + modalidades['nome'].tolist())

fontes = execute_query("SELECT DISTINCT nome FROM dim_fonte ORDER BY nome;")
fonte_selecionada = st.selectbox("Selecione a fonte de recursos:", ["Todas as Fontes"] + fontes['nome'].tolist())

# Modifique a consulta para considerar a seleção da modalidade de licitação, da fonte de recursos e do ano
where_clause = ""
if modalidade_selecionada != "Todas as Modalidades":
    where_clause += f" AND dim_modalidade_licitacao.nome = '{modalidade_selecionada}'"
if fonte_selecionada != "Todas as Fontes":
    where_clause += f" AND dim_fonte.nome = '{fonte_selecionada}'"

query4 = f"""
    SELECT dim_data.ano_nome AS ano,
           dim_modalidade_licitacao.nome AS modalidade,
           dim_fonte.nome AS fonte,
           SUM(fato_pagamento.valor_pago) as total_pago
    FROM fato_pagamento
    JOIN dim_data ON fato_pagamento.cod_tempo = dim_data.keyData
    JOIN dim_modalidade_licitacao ON fato_pagamento.cod_modalidade_licitacao = dim_modalidade_licitacao.key
    JOIN dim_fonte ON fato_pagamento.cod_fonte = dim_fonte.key
    WHERE 1 {where_clause}
    GROUP BY dim_data.ano_nome, dim_modalidade_licitacao.nome, dim_fonte.nome;
"""

result4 = execute_query(query4)

# Exibindo os resultados da Consulta 6
st.write("Valor total pago por modalidade de licitação e fonte de recursos:")
st.dataframe(result4)
connection.close()
