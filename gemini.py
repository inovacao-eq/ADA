import streamlit as st
import pandas as pd
from google import genai
import time

# --- Configuração da Página ---
st.set_page_config(page_title="Gerador em Massa EJ", page_icon="🐷", layout="wide")

st.title("📊 Gerador de Relatórios em Massa - EJ")

st.markdown("Faça upload de uma planilha para gerar descrições para **várias amostras** de uma vez.")

# --- Barra Lateral (Configuração) ---
with st.sidebar:
    st.header("🔑 Acesso")
    api_key = st.text_input("Cole sua API Key do Google:", type="password")
    st.info("Modelo: gemini-2.5-flash")
    
    st.divider()
    st.warning("⚠️ Nota: O processamento pode levar alguns segundos dependendo do tamanho da planilha.")

# --- Função de Geração ---
def gerar_descricao_row(dados_linha, client):
    """Função que recebe uma linha da tabela e chama a IA"""
    prompt = f"""
    Você é um consultor técnico. Com base nos dados técnicos fornecidos abaixo, escreva um parágrafo descritivo para um relatório.
    Seja formal, direto e técnico.
    
    DADOS DA AMOSTRA:
    {dados_linha}
    
    DESCRIÇÃO TÉCNICA:
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro: {e}"

# --- Interface Principal ---

# 1. Upload do Arquivo
uploaded_file = st.file_uploader("Solte seu arquivo aqui (Excel ou CSV)", type=['csv', 'xlsx'])

if uploaded_file and api_key:
    # 2. Ler o arquivo
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("✅ Arquivo carregado com sucesso!")
        st.write("Visualização dos dados:", df.head(3)) # Mostra as 3 primeiras linhas
        
        # 3. Escolher colunas
        colunas_para_ler = st.multiselect(
            "Quais colunas a IA deve ler para criar a descrição?",
            options=df.columns
        )
        
        # 4. Botão de Processar
        if st.button("🚀 Gerar Descrições em Massa"):
            if not colunas_para_ler:
                st.error("Selecione pelo menos uma coluna para a IA ler.")
            else:
                client = genai.Client(api_key=api_key)
                
                # Barra de progresso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                descricoes = []
                total_linhas = len(df)
                
                # Loop por cada linha da planilha
                for index, row in df.iterrows():
                    # Monta o texto apenas com as colunas selecionadas
                    texto_dados = " | ".join([f"{col}: {row[col]}" for col in colunas_para_ler])
                    
                    # Chama a IA
                    resultado = gerar_descricao_row(texto_dados, client)
                    descricoes.append(resultado)
                    
                    # Atualiza barra
                    progress_bar.progress((index + 1) / total_linhas)
                    status_text.text(f"Processando linha {index + 1} de {total_linhas}...")
                
                # Adiciona a nova coluna no DataFrame
                df['Descricao_IA'] = descricoes
                
                st.success("Processamento concluído!")
                
                # Mostra o resultado final
                st.dataframe(df)
                
                # 5. Botão de Download
                # Converte para CSV para download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Planilha Pronta (CSV)",
                    data=csv,
                    file_name="relatorio_gerado_ia.csv",
                    mime="text/csv",
                )
                
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")

elif uploaded_file and not api_key:
    st.warning("Por favor, insira sua API Key na barra lateral.")