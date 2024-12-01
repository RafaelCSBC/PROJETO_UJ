import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from IPython.display import display

# CARREGAR DADOS
tabela = pd.read_csv('dados_att.csv', encoding='utf-8', delimiter=';', on_bad_lines='skip')

dados_rec = pd.read_csv('dados_reciclavel.csv', encoding='utf-8', delimiter=';', on_bad_lines='skip')

#COLUNA EM NUMEROS
tabela['Quantidade Gerada'] = pd.to_numeric(tabela['Quantidade Gerada'], errors='coerce')

dados_rec['Quantidade Gerada'] = pd.to_numeric(dados_rec['Quantidade Gerada'], errors='coerce')


# EMPRESAS ORDEM ALFABETICA
tabela_es = sorted(tabela['Estado'].unique())

#ANO ORDEM CRESCENTE
tabela_ano = tabela.sort_values('Ano da geração', ascending=True).reset_index()

#CONFIG PAGINA
st.set_page_config(
    page_title='E-waste Tracker',
    page_icon=':potted_plant',
    layout='wide',
    initial_sidebar_state='auto',
)

st.subheader('DASHBOARD / ESTADOS')

col1, col2 = st.columns([1,1])

#OPCOES
with col1:
    with st.container():
            opcao_es = st.multiselect(
            'Estado',
            tabela_es
)
with col2:
     with st.container():
        opcao_ano = st.multiselect(
        'Ano',
        tabela_ano['Ano da geração'].unique()
    )
st.warning('Por favor, selecione as opções para aplicar os filtros.')
st.divider()

col3, col4, col5, col6 = st.columns([1,1,1,1])


# TOTAL DE RESIDUOS
with col3:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos (KG)*')
        if opcao_es and opcao_ano:
            dados_filtrados_totalre = tabela[tabela['Estado'].isin(opcao_es) & tabela['Ano da geração'].isin(opcao_ano)
            ]
            soma_total = dados_filtrados_totalre['Quantidade Gerada'].sum()
            soma_formatada = f'{soma_total:_.0f}'.replace('.', ',').replace('_', '.')
            st.markdown(f'**{soma_formatada}**')
        else:    
            pass

# TOTAL RESIDUOS PERIGOSOS
with col4:
    with st.container(border=True):
        st.markdown(f'*Total de Resíduos Perigosos (KG)*')
        if opcao_es and opcao_ano:
            dados_filtrados_totalrp = tabela[
                (tabela['Estado'].isin(opcao_es)) &
                (tabela['Ano da geração'].isin(opcao_ano))
            ]
            
            residuos_perigosos = dados_filtrados_totalrp[
                dados_filtrados_totalrp['Classificação Resíduo'] == 'Perigoso'
            ]
            
            qtd_perigoso = residuos_perigosos['Quantidade Gerada'].sum(skipna=True)
            
            total_perigoso = f'{qtd_perigoso:_.0f}'.replace('.', ',').replace('_', '.')
            st.markdown(f'**{total_perigoso}**')
        else:
            pass

# PRINCIPAL RESIDUO
with col5:
    with st.container(border=True):
        st.markdown(f'*Principal Tipo de Resíduo*')
        if opcao_es and opcao_ano:
            dados_filtrados_prinre = tabela[
                (tabela['Estado'].isin(opcao_es)) & 
                (tabela['Ano da geração'].isin(opcao_ano))
            ]

            # Inicializar tipos como um DataFrame vazio
            tipos = pd.DataFrame()

            if not dados_filtrados_prinre.empty:
                # Remover espaços extras
                dados_filtrados_prinre['Tipo de Resíduo'] = dados_filtrados_prinre['Tipo de Resíduo'].str.strip()
                tipos = dados_filtrados_prinre.groupby('Tipo de Resíduo')['Quantidade Gerada'].sum().reset_index()

            if not tipos.empty:
                top1 = tipos.sort_values('Quantidade Gerada', ascending=False).iloc[0]
                tipo_residuo = top1['Tipo de Resíduo']
                st.markdown(f'**{tipo_residuo}**')
            else:
                pass
        else:
            pass

# PRINCIPAL CIDADE GERADORA
with col6:
    with st.container(border=True):
        st.markdown(f'*Principal Cidade Geradora*')
        if opcao_es and opcao_ano:
            dados_filtrados_cdd = tabela[
                (tabela['Estado'].isin(opcao_es)) & 
                (tabela['Ano da geração'].isin(opcao_ano))
            ]

            cidades = dados_filtrados_cdd.groupby('Município')['Quantidade Gerada'].sum().reset_index()

            if not cidades.empty:
                cidade1 = cidades.sort_values('Quantidade Gerada', ascending=False).iloc[0]
                nome_cdd = cidade1['Município']
                st.markdown(f'**{nome_cdd}**')
            else:
                pass
             
col7, col8 = st.columns([2,2])

#PRINCIPAIS CIDADES GERADORAS
with col7:
    with st.container(border=True):
        st.markdown(f'**Principais Cidades Geradoras**')

        principais_cdd = tabela.groupby(
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

#PRINCIPAIS ESTADOS GERADORES
with col8:
    with st.container(border=True):
        st.markdown(f'**Principais Estados Geradores**')

        # Calcular o total de resíduos gerados por estado
        total_residuos = tabela.groupby('Estado', as_index=False)['Quantidade Gerada'].sum()
        total_residuos.rename(columns={'Quantidade Gerada': 'Resíduos Gerados'}, inplace=True)

        # Filtrar apenas resíduos perigosos
        residuos_perigosos = tabela[tabela['Classificação Resíduo'] == 'Perigoso']

        # Calcular a quantidade de resíduos perigosos por estado
        perigosos_por_estado = residuos_perigosos.groupby('Estado', as_index=False)['Quantidade Gerada'].sum()
        perigosos_por_estado.rename(columns={'Quantidade Gerada': 'Resíduos Perigosos Gerados'}, inplace=True)

        # Combinar as informações em uma única tabela
        resumo = total_residuos.merge(perigosos_por_estado, on='Estado', how='left')

        # Substituir NaN por 0 em "Resíduos Perigosos Gerados"
        resumo['Resíduos Perigosos Gerados'] = resumo['Resíduos Perigosos Gerados'].fillna(0)

         # Ordenar pelo Resíduos Gerados e selecionar os 6 primeiros
        resumo = resumo.sort_values('Resíduos Gerados', ascending=False).head(6)

        # Formatar os valores como texto para exibição formatada
        resumo['Resíduos Gerados'] = resumo['Resíduos Gerados'].apply(
            lambda x: f'{x:_.0f}'.replace('.', ',').replace('_', '.')
        )
        resumo['Resíduos Perigosos Gerados'] = resumo['Resíduos Perigosos Gerados'].apply(
            lambda x: f'{x:_.0f}'.replace('.', ',').replace('_', '.')
        )

        # Exibir a tabela no Streamlit
        st.table(resumo)

# GRAFICO TOTAL RESIDUOS LINHA
with st.container(border=True):
    st.markdown("**Total de Resíduos (KG)**")
    if opcao_es:
        # Aplicar os filtros nos dados
        dados_filtrados = tabela[
        (tabela["Estado"].isin(opcao_es) if opcao_es else True)
        ]

        # Agrupar os dados filtrados por ano e calcular a soma da quantidade gerada
        residuos_por_ano_filtrados = dados_filtrados.groupby('Ano da geração')['Quantidade Gerada'].sum().reset_index()

        # Criar gráfico de linha com cores diferentes para os anos filtrados
        fig_total = px.line(
            residuos_por_ano_filtrados,
            x='Ano da geração',
            y='Quantidade Gerada',
            markers=True,
            color_discrete_sequence=['#636EFA'],
            width=700,
            height=285.5,
            labels={'Quantidade Gerada': 'Quantidade Gerada', 'Ano da geração': 'Ano'}
        )
        st.plotly_chart(fig_total)
    else:
        pass

col9, col10 = st.columns([3,3])

# GRAFICO PERICULOSIDADE
with col9:
    with st.container(border=True):
            st.markdown(f'**Periculosidade dos Resíduos**')
            if opcao_es and opcao_ano:
                dados_filtrados_grafpr = tabela[
                (tabela["Estado"].isin(opcao_es)) &
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
with col10:
    with st.container(border=True):
        st.markdown(f'**Resíduos Potencialmente Recicláveis por Ano**')
        if opcao_es and opcao_ano:
            # Filtrar dados com base nos filtros selecionados
            dados_filtrados_rec = dados_rec[
                (dados_rec['Estado'].isin(opcao_es)) & 
                (dados_rec['Ano da geração'].isin(opcao_ano))
            ]


            # Agrupar por ano e calcular a soma da quantidade gerada
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

            fig_rec.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig_rec.update_layout(
            xaxis=dict(title='Ano'),
            yaxis=dict(title='Quantidade Gerada'))

            # Exibir o gráfico
            st.plotly_chart(fig_rec)

        else:
            pass

# GRAFICO TOTAL RESIDUO PERIGOSO BARRA
with st.container(border=True):
    st.markdown("**Quantidade de Resíduos Perigosos e Não Perigosos por Ano (KG)**")
    if opcao_es and opcao_ano:
        # Aplicar os filtros nos dados
        dados_filtrados = tabela[
            (tabela["Estado"].isin(opcao_es)) &
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