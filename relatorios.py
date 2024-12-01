import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from IPython.display import display

# CARREGAR DADOS
tabela = pd.read_csv("dados_att.csv", encoding='utf-8', delimiter=';', on_bad_lines='skip')

#COLUNA EM NUMEROS
tabela['Quantidade Gerada'] = pd.to_numeric(tabela['Quantidade Gerada'], errors='coerce')

# EMPRESAS ORDEM ALFABETICA
tabela_emp = sorted(tabela['Razao social do gerador'].unique())

#ANO ORDEM CRESCENTE
tabela_ano = tabela.sort_values('Ano da geração', ascending=True).reset_index()

#CONFIG PAGINA
st.set_page_config(
    page_title="E-waste Tracker",
    page_icon=":potted_plant",
    layout="wide",
    initial_sidebar_state="auto",
)

st.subheader('DASHBOARD / EMPRESAS')


#OPCOES
with st.container():
    opcao_ano = st.multiselect(
    "Ano",
    tabela_ano['Ano da geração'].unique())
    
st.warning("Por favor, selecione as opções para os filtros.")
st.divider()

col1, col2, col3, col4 = st.columns([1,1,1,1])

# TOTAL RESIDUOS
with col1:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos (KG)*')
        if opcao_ano:
            dados_filtrados_totalre = tabela[tabela['Ano da geração'].isin(opcao_ano)]

            qtd_totalresi = dados_filtrados_totalre['Quantidade Gerada'].sum()

            qtd_grafico =  dados_filtrados_totalre.groupby('Ano da geração')['Quantidade Gerada'].sum().reset_index()
            fig_resi = px.line(
                qtd_grafico, 
                x='Ano da geração', 
                y='Quantidade Gerada', 
                title='Total de Resíduos', 
                color_discrete_sequence=['#636EFA'],
                markers=True, 
                width=700,
                height=365
            )

            list1 = []
            list1.append(qtd_totalresi)
            for v in list1:
                vl_1 = f'{v:_.0f}'
                val_1 = vl_1.replace('.',',').replace('_','.')
                st.markdown(f'**{val_1}**')
        else:    
            pass
        
# TOTAL EMPRESAS
with col2:
    with st.container(border=True):
        st.markdown(f'*Total de Empresas*')
        if opcao_ano:
            dados_filtrados_totalemp = tabela[tabela['Ano da geração'].isin(opcao_ano)]

            n_empresas = dados_filtrados_totalemp['Razao social do gerador'].nunique()
            st.markdown(f'**{n_empresas}**')
        else:
            pass

# TOTAL RESIDUOS PERIGOSOS
with col3:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos Perigosos (KG)*')
        if opcao_ano:
            dados_filtrados_totalerp = tabela[tabela['Ano da geração'].isin(opcao_ano)]

            perigoso = tabela.loc[tabela['Classificação Resíduo'] == 'Perigoso']
            qtd_perigoso = perigoso['Quantidade Gerada'].sum()

            list_pg = []
            list_pg.append(qtd_perigoso)
            for v in list_pg:
                vl_pg = f'{v:_.0f}'
                val_pg = vl_pg.replace('.',',').replace('_','.')
            st.markdown(f'**{val_pg}**')
        else:
            pass

# ESTADO MAIOR GERACAO
with col4:
    with st.container(border=True):
        st.markdown(f'*Principal Estado Gerador*')
        if opcao_ano:
            dados_filtrados_totalmg = tabela[tabela['Ano da geração'].isin(opcao_ano)]

            estado_ger = dados_filtrados_totalmg.groupby('Estado')['Quantidade Gerada'].sum().reset_index()

            if not estado_ger.empty:
                estado1 = estado_ger.sort_values('Quantidade Gerada',ascending=False).iloc[0]
                nome_est = estado1['Estado']
                st.markdown(f"**{nome_est}**")

        else:
            pass

col5, col6 = st.columns([2,2])

# PRINCIPAIS CIDADES GERADORAS
with col5:
    with st.container(border=True):
        st.markdown(f"**Principais Cidades Geradoras**")
        if opcao_ano:
            dados_filtrados_totalpcdd = tabela[tabela['Ano da geração'].isin(opcao_ano)]

            principais_cdd = dados_filtrados_totalpcdd.groupby(
                ['Município', 'Estado'], as_index=False
            )['Quantidade Gerada'].sum()

            principais_cdd = principais_cdd.sort_values(
                'Quantidade Gerada', ascending=False
            ).head(6)

            # Criar coluna formatada para exibição
            principais_cdd['Quantidade Gerada'] = principais_cdd['Quantidade Gerada'].apply(
                    lambda x: f'{x:_.0f}'.replace('.', ',').replace('_', '.')
            )

            # Exibir apenas as colunas desejadas
            colunas_exibir = ['Município', 'Estado', 'Quantidade Gerada']
            st.table(principais_cdd[colunas_exibir])
        else:
            pass

#PRINCIPAIS ESTADOS GERADORES
with col6:
    with st.container(border=True):
        st.markdown(f"**Principais Estados Geradores**")
        if opcao_ano:
            dados_filtrados= tabela[tabela['Ano da geração'].isin(opcao_ano)]

             # Calcular o total de resíduos gerados por estado
            total_residuos = dados_filtrados.groupby('Estado', as_index=False)['Quantidade Gerada'].sum()
            total_residuos.rename(columns={'Quantidade Gerada': 'Resíduos Gerados'}, inplace=True)

            total_residuos = total_residuos.sort_values('Resíduos Gerados', ascending=False).head(6)

            # Formatar os valores como texto para exibição formatada
            total_residuos['Resíduos Gerados'] = total_residuos['Resíduos Gerados'].apply(
                lambda x: f'{x:_.0f}'.replace('.', ',').replace('_', '.')
            )

            st.table(total_residuos)
        else:
            pass

col7, col8 = st.columns([3,3])

# BARRA RESIDUO POR ESTADO
with col7:
    with st.container(border=True):
        st.markdown("**Resíduos por Estado (KG)**")
        if opcao_ano:
            # Aplicar os filtros nos dados
            dados_filtrados = tabela[
            (tabela["Ano da geração"].isin(opcao_ano) if opcao_ano else True)
            ]

            lixo_estado = dados_filtrados.groupby('Estado')['Quantidade Gerada'].sum().reset_index()

            fig3 = px.bar(
                lixo_estado,
                title='Resíduos por Estado',
                x = 'Estado',
                y = 'Quantidade Gerada',
                color = 'Estado',
                color_discrete_sequence=px.colors.qualitative.Plotly,  # Paleta de cores
                height=300
            )

            # Exibir o gráfico
            st.plotly_chart(fig3)
        else:
            pass

# PERICULOSIDADE DOS RESIDUOS
with col8:
    with st.container(border=True):
        st.markdown(f'**Periculosidade dos Resíduos**')
        if opcao_ano:
            dados_filtrados = tabela[
            (tabela["Ano da geração"].isin(opcao_ano) if opcao_ano else True)
            ]

            perigo_resi = dados_filtrados.loc[dados_filtrados['Classificação Resíduo'].isin(['Perigoso','Não Perigoso'])].groupby('Classificação Resíduo')['Quantidade Gerada'].sum().reset_index()

            # Criando o gráfico de setores
            perigo_grafico = px.pie(
            perigo_resi, 
            names='Classificação Resíduo', 
            values='Quantidade Gerada',
            color='Classificação Resíduo',
            color_discrete_map={'Perigoso': '#FF6347', 'Não Perigoso': '#4682B4'},
            height=300,
            width=400
            )

            st.plotly_chart(perigo_grafico)
        else:
            pass
                    
# RESIDUOS POR ANO
with st.container(border=True):
    # Verificar se há filtros selecionados
    st.markdown("**Resíduos por Ano (KG)**")

        # Agrupar os dados filtrados por ano e calcular a soma da quantidade gerada
    residuos_por_ano_filtrados = tabela.groupby('Ano da geração')['Quantidade Gerada'].sum().reset_index()

        # Criar gráfico de barras com cores diferentes para os anos filtrados
    fig_barras_filtradas = px.bar(
            residuos_por_ano_filtrados,
            x='Ano da geração',
            y='Quantidade Gerada',
            labels={'Ano da geração': 'Ano', 'Quantidade Gerada': 'Quantidade de Resíduos'},
            color='Ano da geração',
            text='Quantidade Gerada',  # Adiciona os valores nas barras
            color_discrete_sequence=px.colors.qualitative.Pastel  # Paleta de cores
        )

        # Ajustar layout do gráfico
    fig_barras_filtradas.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_barras_filtradas.update_layout(
        xaxis=dict(title='Ano'),
        yaxis=dict(title='Quantidade Gerada')
    )

        # Exibir o gráfico
    st.plotly_chart(fig_barras_filtradas)

