import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from IPython.display import display

# CARREGAR DADOS
tabela = pd.read_csv("dados_att.csv", encoding='utf-8', delimiter=';', on_bad_lines='skip')

dados_rec = pd.read_csv('dados_reciclavel.csv', encoding='utf-8', delimiter=';', on_bad_lines='skip')

#COLUNA EM NUMEROS
tabela['Quantidade Gerada'] = pd.to_numeric(tabela['Quantidade Gerada'], errors='coerce')

dados_rec['Quantidade Gerada'] = pd.to_numeric(dados_rec['Quantidade Gerada'], errors='coerce')

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

col1, col2 = st.columns([1,1])

#OPCOES
with col1:
    with st.container():
            opcao_emp = st.multiselect(
            "Empresas",
            tabela_emp
)
with col2:
     with st.container():
        opcao_ano = st.multiselect(
        "Ano",
        tabela_ano['Ano da geração'].unique()
    )
st.warning("Por favor, selecione as opções para os filtros.")
st.divider()

col3, col4, col5 = st.columns([1,1,1])


# TOTAL DE RESIDUOS
with col3:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos (KG)*')
        if opcao_emp and opcao_ano:
            dados_filtrados_totalre = tabela[tabela["Razao social do gerador"].isin(opcao_emp) & tabela["Ano da geração"].isin(opcao_ano)
            ]

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

# TOTAL RESIDUOS PERIGOSOS
with col4:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos Perigosos (KG)*')
        if opcao_emp and opcao_ano:
            dados_filtrados_totalrp = tabela[
                (tabela["Razao social do gerador"].isin(opcao_emp)) &
                (tabela["Ano da geração"].isin(opcao_ano))
            ]
            
            residuos_perigosos = dados_filtrados_totalrp[
                dados_filtrados_totalrp['Classificação Resíduo'] == 'Perigoso'
            ]
            
            qtd_perigoso = residuos_perigosos['Quantidade Gerada'].sum()
            
            val_perigoso = f'{qtd_perigoso:_.0f}'.replace('.', ',').replace('_', '.')
            st.markdown(f'**{val_perigoso}**')
        else:
            pass

# PRINCIPAL RESIDUO
with col5:
    with st.container(border=True):
        st.markdown(f'*Principal Tipo de Resíduo*')
        if opcao_emp and opcao_ano:
            dados_filtrados_prinre = tabela[
                (tabela["Razao social do gerador"].isin(opcao_emp)) &
                (tabela["Ano da geração"].isin(opcao_ano))
            ]

            if not dados_filtrados_prinre.empty:
                # Remover espaços extras
                dados_filtrados_prinre['Tipo de Resíduo'] = dados_filtrados_prinre['Tipo de Resíduo'].str.strip()
                tipos = dados_filtrados_prinre.groupby('Tipo de Resíduo')['Quantidade Gerada'].sum().reset_index()

                if not tipos.empty:
                    top1 = tipos.sort_values('Quantidade Gerada', ascending=False).iloc[0]
                    tipo_residuo = top1["Tipo de Resíduo"]
                    st.markdown(f'**{tipo_residuo}**')
        else:
            pass

col6, col7 = st.columns([2,2])

# TABELA PRINCIPAIS TIPOS DE RESIDUOS
with col6:
    with st.container(border=True):
        st.markdown(f'**Principal Tipos de Resíduo**')
        if opcao_emp and opcao_ano:
            dados_filtrados_printa = tabela[
                (tabela["Razao social do gerador"].isin(opcao_emp)) &
                (tabela["Ano da geração"].isin(opcao_ano))
            ]

            principais = dados_filtrados_printa.groupby('Tipo de Resíduo')['Quantidade Gerada'].sum().reset_index()

            # Ordenar em ordem decrescente e selecionar os 6 primeiros
            principais = principais.sort_values('Quantidade Gerada', ascending=False).head(6)

            # Criar uma lista com os nomes dos tipos de resíduos
            lista_tipos = principais['Tipo de Resíduo'].tolist()

            # Exibir a lista como um DataFrame para visualização
            df_formatado = pd.DataFrame({'Tipo de Resíduo': lista_tipos})

            st.table(df_formatado)
        else:
            pass

# GRAFICO TOTAL DE RESIDUOS
with col7:
    with st.container(border=True):
        st.markdown(f'**Total de Resíduos**')
        if opcao_emp and opcao_ano:
            dados_filtrados_grafre = tabela[tabela["Razao social do gerador"].isin(opcao_emp) & tabela["Ano da geração"].isin(opcao_ano)]

            qtd_grafico = dados_filtrados_grafre.groupby('Ano da geração')['Quantidade Gerada'].sum().reset_index()

            fig_resi = px.line(
                qtd_grafico,
                x='Ano da geração',
                y='Quantidade Gerada',
                markers=True,
                color_discrete_sequence=['#636EFA'],
                width=700,
                height=275,
                labels={'Quantidade Gerada': 'Quantidade Gerada', 'Ano da geração': 'Ano'},
            )
            st.plotly_chart(fig_resi)
        else:
            pass

col8, col9 = st.columns([3,3])

# PERICULOSIDADE DOS RESIDUOS
with col8:
    with st.container(border=True):
        st.markdown(f'**Periculosidade dos Resíduos**')
        if opcao_emp and opcao_ano:
            dados_filtrados_grafpr = tabela[
            (tabela["Razao social do gerador"].isin(opcao_emp)) &
            (tabela["Ano da geração"].isin(opcao_ano))
            ]

            perigo_resi = dados_filtrados_grafpr.loc[dados_filtrados_grafpr['Classificação Resíduo'].isin(['Perigoso','Não Perigoso'])].groupby('Classificação Resíduo')['Quantidade Gerada'].sum().reset_index()

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

# GRAFICO RESIDUOS RECICLAVEIS
with col9:
    with st.container(border=True):
        st.markdown(f'**Resíduos Potencialmente Recicláveis por Ano**')
        if opcao_emp and opcao_ano:
            dados_filtrados_rec = dados_rec[
            (tabela["Razao social do gerador"].isin(opcao_emp)) &
            (tabela["Ano da geração"].isin(opcao_ano))
            ]

            tabela_rec = dados_filtrados_rec.groupby(
                'Ano da geração', as_index=False
            )['Quantidade Gerada'].sum()

            # Criar o gráfico de barras
            fig_rec = px.bar(
                tabela_rec,
                x='Ano da geração',
                y='Quantidade Gerada',
                labels={'Quantidade Gerada': 'Quantidade Gerada', 'Ano da geração': 'Ano'},
                text='Quantidade Gerada',
                height=300
            )

            # Ajustar layout do gráfico
            fig_rec.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig_rec.update_layout(
            xaxis=dict(title='Ano'),
            yaxis=dict(title='Quantidade Gerada'))

            # Exibir o gráfico
            st.plotly_chart(fig_rec)

        else:
            pass



#GRAFICO RESIDUOS PERIGOSOS POR ANO
with st.container(border=True):
    st.markdown("**Quantidade de Resíduos Perigosos e Não Perigosos por Ano (KG)**")
    if opcao_emp and opcao_ano:
        # Aplicar os filtros nos dados
        dados_filtrados = tabela[
            (tabela["Razao social do gerador"].isin(opcao_emp)) &
            (tabela["Ano da geração"].isin(opcao_ano))
        ]

        # Agrupar os dados filtrados por ano e classificação de resíduo
        residuos_perigosos_por_ano = (
            dados_filtrados.loc[dados_filtrados['Classificação Resíduo'].isin(['Perigoso', 'Não Perigoso'])]
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
    else:
        pass







