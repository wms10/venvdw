
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

st.title('Pergunta 1')
st.subheader('Qual a porcentagem de valor pago por modalidade, e a diferença do valor pago para o empenhado?')

# Consulta 1: Porcentagem de valor pago por modalidade e diferença para empenhado
# Adicione um menu suspenso para selecionar a modalidade
modalidades = execute_query("SELECT DISTINCT nome FROM dim_modalidade_licitacao ORDER BY nome;")
modalidade_selecionada = st.selectbox("Selecione a modalidade:", ["Todas as Modalidades"] + modalidades['nome'].tolist())

# Modifique a consulta para considerar a seleção da modalidade
if modalidade_selecionada == "Todas as Modalidades":
    query1 = """
        SELECT dim_modalidade_licitacao.nome,
               SUM(fato_pagamento.valor_pago) / SUM(fato_pagamento.valor_empenhado) * 100 as porcentagem_pago,
               SUM(fato_pagamento.valor_pago) - SUM(fato_pagamento.valor_empenhado) as diferenca
        FROM fato_pagamento
        JOIN dim_modalidade_licitacao ON fato_pagamento.cod_modalidade_licitacao = dim_modalidade_licitacao.codigo
        GROUP BY dim_modalidade_licitacao.nome;
    """
else:
    query1 = f"""
        SELECT dim_modalidade_licitacao.nome,
               SUM(fato_pagamento.valor_pago) / SUM(fato_pagamento.valor_empenhado) * 100 as porcentagem_pago,
               SUM(fato_pagamento.valor_pago) - SUM(fato_pagamento.valor_empenhado) as diferenca
        FROM fato_pagamento
        JOIN dim_modalidade_licitacao ON fato_pagamento.cod_modalidade_licitacao = dim_modalidade_licitacao.codigo
        WHERE dim_modalidade_licitacao.nome = '{modalidade_selecionada}'
        GROUP BY dim_modalidade_licitacao.nome;
    """

result1 = execute_query(query1)

# Exibindo os resultados da Consulta 1
st.write(f"Resultados para a modalidade: {modalidade_selecionada}")
st.dataframe(result1)
connection.close()
