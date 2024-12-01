import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from IPython.display import display

#CONFIG PAGINA
st.set_page_config(
    page_title="E-waste Tracker",
    page_icon=":potted_plant",
    layout="wide",
    initial_sidebar_state="auto",
)

st.subheader('DASHBOARD / GERAL')
st.divider()

# CARREGAR DADOS
tabela = pd.read_csv("dados_att.csv", encoding='utf-8', delimiter=';', on_bad_lines='skip')

# TOTAL RESIDUOS
tabela['Quantidade Gerada'] = pd.to_numeric(tabela['Quantidade Gerada'], errors='coerce')
soma_res = tabela['Quantidade Gerada'].sum()
list_tr = []
list_tr.append(soma_res)
for v in list_tr:
    vl_tr = f'{v:_.0f}'
    val_tr = vl_tr.replace('.',',').replace('_','.')

# TOTAL EMPRESAS
n_empresas = tabela['Razao social do gerador'].nunique()

# TOTAL RESIDUOS PERIGOSOS
perigoso = tabela.loc[tabela['Classificação Resíduo'] == 'Perigoso']
qtd_perigoso = perigoso['Quantidade Gerada'].sum()
list_pg = []
list_pg.append(qtd_perigoso)
for v in list_pg:
    vl_pg = f'{v:_.0f}'
    val_pg = vl_pg.replace('.',',').replace('_','.')

# ESTADO MAIOR GERACAO
estado_ger = tabela['Estado'].unique()
result={}
for item in estado_ger:
    tab = tabela.loc[tabela['Estado']== item]
    tot_tab = tab['Quantidade Gerada'].sum()
    result[item] = tot_tab
estado_maior_ger = max(result, key=result.get)

col1, col2, col3, col4 = st.columns([1,1,1,1])

#RESIDUOS MAIS GERADOS

#TIPOS DE RESIDUOS
# Agrupando por tipo de resíduo e calculando a soma
total_por_tipo = tabela.groupby('Tipo de Resíduo')['Quantidade Gerada'].sum().reset_index()

# Ordenando em ordem decrescente e selecionando os 6 primeiros
top_6_residuos = total_por_tipo.sort_values('Quantidade Gerada', ascending=False).head(6)
# Criando uma lista para armazenar os valores formatados
lista_top_6 = []

# Iterando sobre os 5 primeiros e formatando os valores
for _, row in top_6_residuos.iterrows():
    valor_formatado = f'{row["Quantidade Gerada"]:_.0f}'
    valor_formatado = valor_formatado.replace('.', ',').replace('_', '.')
    lista_top_6.append(valor_formatado)
top_6_residuos['Quantidade Gerada'] = lista_top_6

# GRAFICO GERACAO RESÍDUOS
# Agrupar os dados por ano e calcular a soma da quantidade gerada
total_por_ano = tabela.groupby('Ano da geração')['Quantidade Gerada'].sum().reset_index()
fig_1 = px.line(
    total_por_ano, 
    x='Ano da geração', 
    y='Quantidade Gerada', 
    title='Total de Resíduos', 
    color_discrete_sequence=['#636EFA'],
    markers=True, 
    width=700,
    height=405,
    labels={'Quantidade Gerada': 'Quantidade Gerada', 'Ano da geração': 'Ano'}
)

#GRAFICO SETOR TIPO DE RESIDUO
# Filtrando apenas para categorias 'Perigoso' e 'Não Perigoso'
tipo_residuo = tabela.loc[tabela['Classificação Resíduo'].isin(['Perigoso', 'Não Perigoso'])].groupby('Classificação Resíduo')['Quantidade Gerada'].sum().reset_index()

# Criando o gráfico de setores
fig2 = px.pie(
    tipo_residuo, 
    title='Periculosidade dos Resíduos',
    names='Classificação Resíduo', 
    values='Quantidade Gerada',
    color='Classificação Resíduo',
    color_discrete_map={'Perigoso': '#FF6347', 'Não Perigoso': '#4682B4'},
    height=300,
    width=400
)

#GRAFICO RESIDUOS POR ESTADO
lixo_estado = tabela.groupby('Estado')['Quantidade Gerada'].sum().reset_index()
fig3 = px.bar(
    lixo_estado,
    title='Resíduos por Estado',
    x = 'Estado',
    y = 'Quantidade Gerada',
    color = 'Estado',
    color_discrete_sequence=px.colors.qualitative.Plotly,  # Paleta de cores
    height=300
)

with col1:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos (KG)*')
        st.markdown(f'**{val_tr}** ')
with col2:
    with st.container(border=True):
        st.markdown(f'*Total de Empresas*')
        st.markdown(f'**{n_empresas}**')
with col3:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos Perigosos (KG)*')
        st.markdown(f'**{val_pg}** ')
with col4:
    with st.container(border=True):
        st.markdown(f'*Principal Estado Gerador*')
        st.markdown(f'**{estado_maior_ger}**')
        
col5, col6 = st.columns([2,2])

with col5:
    with st.container(border=True):
        st.plotly_chart(fig_1)
with col6:
    with st.container(border=True):
        st.markdown(f'**Principais Tipos de Resíduos**')
        st.table(top_6_residuos)

col7, col8 = st.columns([3,3])

with col7:
    with st.container(border=True):
        st.plotly_chart(fig3)
with col8:
     with st.container(border=True):
        st.plotly_chart(fig2)

# Gráfico de barras de resíduos por ano (geral, sem filtros)
with st.container(border=True):
    st.markdown("**Quantidade de Resíduos Perigosos e Não Perigosos por Ano (KG)**")

        # Agrupar os dados filtrados por ano e classificação de resíduo
    residuos_perigosos_por_ano = (
            tabela.loc[tabela['Classificação Resíduo'].isin(['Perigoso', 'Não Perigoso'])]
            .groupby(['Ano da geração', 'Classificação Resíduo'])['Quantidade Gerada']
            .sum()
            .reset_index()
        )

        # Criar gráfico de barras com cores diferentes para os tipos de resíduos
    fig_barras_filtradas = px.bar(
            residuos_perigosos_por_ano,
            x='Ano da geração',
            y='Quantidade Gerada',
            color='Classificação Resíduo',
            text='Quantidade Gerada',  # Adiciona os valores nas barras
            labels={
                'Ano da geração': 'Ano',
                'Quantidade Gerada': 'Quantidade de Resíduos'
            },
            color_discrete_map={'Perigoso': '#FF6347', 'Não Perigoso': '#4682B4'},  # Paleta de cores
        )

        # Ajustar layout do gráfico
    fig_barras_filtradas.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_barras_filtradas.update_layout(
            xaxis=dict(title='Ano'),
            yaxis=dict(title='Quantidade Gerada')
        )

        # Exibir o gráfico
    st.plotly_chart(fig_barras_filtradas)



    





