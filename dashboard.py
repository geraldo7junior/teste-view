# python -m streamlit run app.py

# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Título do dashboard
st.title("Dashboard de Vendas de Celulares")

# Caminho do arquivo CSV na mesma pasta
csv_file = 'Cellphone_Sales_Data.csv'

# Verifica se o arquivo CSV existe na mesma pasta
if os.path.exists(csv_file):
    # Lê o arquivo CSV em um DataFrame
    df = pd.read_csv(csv_file)

    # Exibe os dados carregados
    st.markdown("### Dados de Vendas Carregados")
    st.dataframe(df.head())

    # Conversão da coluna "Date" para formato de data
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    # Filtros de seleção
    st.sidebar.header("Filtros")
    selected_store = st.sidebar.multiselect("Selecione a Loja", options=df['Store'].unique(), default=df['Store'].unique())
    selected_model = st.sidebar.multiselect("Selecione o Modelo de Celular", options=df['Cellphone Model'].unique(), default=df['Cellphone Model'].unique())
    selected_date_range = st.sidebar.date_input("Selecione o Período", [df['Date'].min(), df['Date'].max()])

    # Filtragem dos dados com base na seleção do usuário
    filtered_df = df[(df['Store'].isin(selected_store)) & 
                     (df['Cellphone Model'].isin(selected_model)) &
                     (df['Date'] >= pd.to_datetime(selected_date_range[0])) & 
                     (df['Date'] <= pd.to_datetime(selected_date_range[1]))]

    # Exibe os dados filtrados
    st.markdown("### Dados Filtrados")
    st.dataframe(filtered_df)

    # Insights gerais
    st.markdown("## Insights Gerais")
    total_sales = filtered_df['Total Sales'].sum()
    total_quantity = filtered_df['Quantity Sold'].sum()
    st.write(f"**Total de Vendas:** R$ {total_sales:,.2f}")
    st.write(f"**Total de Unidades Vendidas:** {total_quantity}")

    # Gráfico de vendas por modelo
    st.markdown("### Vendas por Modelo de Celular")
    sales_by_model = filtered_df.groupby('Cellphone Model')['Total Sales'].sum().sort_values(ascending=False)
    st.bar_chart(sales_by_model)

    # Gráfico de vendas por loja
    st.markdown("### Vendas por Loja")
    sales_by_store = filtered_df.groupby('Store')['Total Sales'].sum().sort_values(ascending=False)
    st.bar_chart(sales_by_store)

    # Gráfico de vendas ao longo do tempo
    st.markdown("### Evolução das Vendas ao Longo do Tempo")
    sales_over_time = filtered_df.groupby('Date')['Total Sales'].sum()
    st.line_chart(sales_over_time)

    # Média de preços por modelo de celular
    st.markdown("### Preço Médio por Modelo de Celular")
    avg_price_by_model = filtered_df.groupby('Cellphone Model')['Unit Price'].mean().sort_values(ascending=False)
    st.bar_chart(avg_price_by_model)

    # Explicação do Streamlit
    st.markdown("## Sobre o Streamlit")
    st.write("""
    **Streamlit** é uma biblioteca de Python de código aberto que permite criar e compartilhar aplicativos de dados 
    interativos de forma fácil e rápida. Ela transforma scripts em uma interface de usuário web amigável e intuitiva 
    sem a necessidade de conhecimento em desenvolvimento web. Abaixo estão os principais conceitos utilizados neste exemplo:

    - `st.title()`: Adiciona um título ao seu aplicativo.
    - `st.markdown()`: Permite adicionar textos em formato Markdown.
    - `st.dataframe()`: Exibe um DataFrame do Pandas.
    - `st.sidebar`: Permite adicionar componentes de entrada e seleção na barra lateral do aplicativo.
    - `st.multiselect()`: Adiciona uma caixa de seleção múltipla.
    - `st.date_input()`: Adiciona um componente de seleção de data.
    - `st.bar_chart()`: Cria um gráfico de barras.
    - `st.line_chart()`: Cria um gráfico de linha.
    """)

else:
    st.write(f"Arquivo '{csv_file}' não encontrado. Por favor, coloque o arquivo na mesma pasta que este script.")
