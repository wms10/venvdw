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

st.title('Pergunta 2')

st.subheader('Qual o valor total liquidado e empenhado filtrado por órgão?')


# Consulta 2: Valor total liquidado e empenhado filtrado por órgão
# Adicione um menu suspenso para selecionar o órgão
orgaos = execute_query("SELECT DISTINCT nome FROM dim_empenho ORDER BY nome;")
orgao_selecionado = st.selectbox("Selecione o órgão:", ["Todos os Órgãos"] + orgaos['nome'].tolist())

# Modifique a consulta para considerar a seleção do órgão
if orgao_selecionado == "Todos os Órgãos":
    query2 = """
        SELECT dim_empenho.nome, 
               SUM(fato_pagamento.valor_empenhado) as total_empenhado,
               SUM(fato_pagamento.valor_pago) as total_pago
        FROM fato_pagamento
        JOIN dim_empenho ON fato_pagamento.cod_empenho = dim_empenho.codigo
        GROUP BY dim_empenho.nome;
    """
else:
    query2 = f"""
        SELECT dim_empenho.nome, 
               SUM(fato_pagamento.valor_empenhado) as total_empenhado,
               SUM(fato_pagamento.valor_pago) as total_pago
        FROM fato_pagamento
        JOIN dim_empenho ON fato_pagamento.cod_empenho = dim_empenho.codigo
        WHERE dim_empenho.nome = '{orgao_selecionado}'
        GROUP BY dim_empenho.nome;
    """

result2 = execute_query(query2)

# Exibindo os resultados da Consulta 2
st.write("Valor total liquidado e empenhado filtrado por órgão:")
st.dataframe(result2)
connection.close()
