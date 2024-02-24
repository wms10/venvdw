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

st.title('Pergunta 3')

st.subheader('Qual é o total liquidado e empenhado por ação e credor, considerando um período específico?')

# Adicione menus suspensos para selecionar a ação, o credor e o período
acoes = execute_query("SELECT DISTINCT nome FROM dim_acao ORDER BY nome;")
acao_selecionada = st.selectbox("Selecione a ação:", ["Todas as Ações"] + acoes['nome'].tolist())

credores = execute_query("SELECT DISTINCT nome FROM dim_credor ORDER BY nome;")
credor_selecionado = st.selectbox("Selecione o credor:", ["Todos os Credores"] + credores['nome'].tolist())

# Modifique a consulta para considerar a seleção da ação, do credor e do período
where_clause = ""
if acao_selecionada != "Todas as Ações":
    where_clause += f" AND dim_acao.nome = '{acao_selecionada}'"
if credor_selecionado != "Todos os Credores":
    where_clause += f" AND dim_credor.nome = '{credor_selecionado}'"

query3 = f"""
    SELECT dim_data.mes_nome AS mes,
           dim_acao.nome AS acao,
           dim_credor.nome AS credor,
           SUM(fato_pagamento.valor_empenhado) as total_empenhado,
           SUM(fato_pagamento.valor_pago) as total_pago
    FROM fato_pagamento
    JOIN dim_data ON fato_pagamento.cod_tempo = dim_data.keyData
    JOIN dim_acao ON fato_pagamento.cod_acao = dim_acao.key
    JOIN dim_credor ON fato_pagamento.cod_credor = dim_credor.key
    WHERE 1 {where_clause}
    GROUP BY dim_data.mes_nome, dim_acao.nome, dim_credor.nome;
"""

result3 = execute_query(query3)

# Exibindo os resultados da Consulta 5
st.write("Valor total liquidado e empenhado por ação e credor:")
st.dataframe(result3)
connection.close()
