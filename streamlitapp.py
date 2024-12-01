import streamlit as st

#setup pagina
geral_p = st.Page(
    page='views/dash.py',
    title='🌍 Geral',
    default=True,
)

empresas_p = st.Page(
    page='views/empresas.py',
    title='🏭 Empresas',
)

estados_p = st.Page(
    page='views/estados.py',
    title='🗺️ Estados',
)

relatorios_p = st.Page(
    page='views/relatorios.py',
    title='📄 Relatórios',
)

pg = st.navigation(
    {
        'Dashboards':[geral_p, empresas_p, estados_p],
        'Relatórios':[relatorios_p]
    }
)

pg.run()