import streamlit as st
import pandas as pd
from google import genai
import time

st.set_page_config(page_title="Descrição Amostral", page_icon="🐷", layout="wide")

st.title("🐷 Descrição Amostral - EQ")

st.markdown("Adquira gratuitamente sua chave de API aqui: https://aistudio.google.com/api-keys")

st.markdown("Qualquer dúvida, basta entrar em contato com a equipe de Inovação!")

st.divider()

st.subheader("Faça upload de uma planilha para gerar descrições para **várias amostras** de uma vez:")


with st.sidebar:
    st.header("🔑 Acesso")
    api_key = st.text_input("Cole sua API Key do Google:", type="password")
    st.info("Modelo: gemini-3.1-flash-lite")
    
    st.divider()
    st.warning("⚠️ Nota: O processamento pode levar alguns minutos dependendo do tamanho da planilha.")
    
def gerar_descricao_row(dados_linha, client, total_amostras):
    prompt = f"""
    Você é um consultor técnico experiente e analista de dados. Sua tarefa é redigir o parágrafo descritivo de uma amostra para um relatório técnico acadêmico/corporativo.

    DIRETRIZES RÍGIDAS:

    Use linguagem formal, técnica, impessoal e direta.

    NÃO INVENTE DADOS OU TIRE CONCLUSÕES FORA DA TABELA. Baseie-se exclusivamente nos números fornecidos na entrada.

    NÃO FAÇA CÁLCULOS MATEMÁTICOS. Utilize apenas as quantidades e porcentagens já fornecidas no texto de entrada.

    Cite sempre os números absolutos acompanhados de suas respectivas porcentagens para embasar as afirmações.

    Siga rigorosamente o tom e a estrutura dos exemplos abaixo.

    O tamanho total da amostra é: {total_amostras}.


    ### EXEMPLO 1
    Entrada: Gênero Qtd. Repres.
    Masculino 35 19,66%
    Feminino 143 80,34%
    Total Geral 178 100,00%a
    Saída: A amostra, demonstrada na tabela acima, revela que a maioria dos respondentes se identifica com o gênero feminino, totalizando 143 participantes. Em segundo lugar, 35 respondentes se identificaram com o gênero masculino, evidenciando uma presença masculina menor em comparação à feminina. Esses dados apontam para uma predominância feminina.

    ### EXEMPLO 2
    Entrada: Qual sua idade? Valores
    18 - 24 anos 15
    25 - 35 anos 47
    36 - 45 anos 25
    46 - 59 anos 12
    60 anos ou mais 3
    Total geral 102
    Saída: Em relação a idade da amostra, pode-se analisar que a maioria dos entrevistados são jovens entre 25 a 35 anos, os quais totalizam 46,1% da amostra. Além disso, foi observada uma considerável presença de pessoas com idades entre 36 e 45 anos, representando 24,5% do conjunto de entrevistados. Em seguida, destacam-se os participantes com idades entre 18 e 24 anos, os quais totalizam 14,7% dos 102 respondentes analisados. Por outro lado, as faixas etárias mais velhas, particularmente aquelas com mais de 46 anos, foram as menos presentes na amostra, de 46 a 59 tiveram 12 entrevistados (11,8%) e apenas 3 na faixa etária acima de 60 anos (2,9%). Portanto, é possível concluir que a amostra tende a englobar predominantemente indivíduos de idade mais jovem.

    ### EXEMPLO 3
    Entrada: Renda Qtd. Repres.
    Até R$2.000 46 25,84%
    R$ 2.001 a R$
    3.000 22 12,36%
    R$ 3.001 a R$
    6.000 33 18,54%
    R$ 6.001 a R$
    8.000 20 11,24%
    Acima de R$
    8.001 57 32,02%
    Total geral 178 100,00%
    Saída: A amostra apresentada demonstra que a maioria dos respondentes possui renda superior a R$8.001, representando 32,02% do total. Em segundo lugar, estão as pessoas com renda de até R$2.000, correspondendo a 25,84% da amostra. Observa-se que a distribuição de renda da amostra é bastante dispersa entre as faixas analisadas; contudo, percebe-se uma maior concentração nos extremos da distribuição.

    ### EXEMPLO 4
    Entrada: Bairros Qtd. Repres.
    Petrópolis 21 11,80%
    Centro Histórico 10 5,62%
    Bom Fim 8 4,49%
    Jardim Isabel 6 3,37%
    Jardim Botânico 6 3,37%
    Teresópolis 5 2,81%
    Rio Branco 5 2,81%
    Passo d’Areia 5 2,81%
    Jardim Europa 5 2,81%
    Belém Novo 5 2,81%
    Sarandi 4 2,25%
    Partenon 4 2,25%
    Floresta 4 2,25%
    Boa Vista 4 2,25%
    Bela Vista 4 2,25%
    Outros 82 46,07%
    Saída: A tabela acima apresenta a distribuição das respostas pelos bairros. O bairro com maior concentração é Petrópolis, com 21 registros, representando 11,80% do total. Em seguida, destacam-se Centro Histórico com 10 ocorrências (5,62%) e Bom Fim com 8 (4,49%). Outros bairros aparecem com menor frequência, variando entre 2,25% e 3,37% cada. Todavia, a maior parte dos registros está agrupada por “Outros”, com 82 estabelecimentos, o que corresponde a 46,07% da amostra, o que pode indicar o interesse do assunto da pesquisa pelo público que não se restringe a um local específico.

    ### EXEMPLO 5
    Entrada: No mês passado, quantas vezes você saiu para bares e/ou festas? Valores
    Nenhuma vez 12
    1 vez 10
    2 vezes 16
    3 vezes 12
    4 vezes 9
    5 vezes 9
    6 vezes 5
    7 vezes 2
    8 vezes 6
    10 vezes 2
    Mais de 10 vezes 16
    Total geral 99
    Saída: A análise da tabela revela uma distribuição variada das respostas sobre o número de saídas para bares e/ou festas no último mês. A maioria dos participantes relatou uma frequência moderada de saídas, com valores concentrados entre uma e três vezes, representando aproximadamente 57% das respostas (38 entrevistados). Porém, altas frequências, como mais de dez vezes, também tiveram uma parcela significativa da amostra, 16 entrevistados (16,2%). As frequências um pouco mais altas, como quatro, cinco e sete, surgiram com menor frequência, indicando que uma parcela menor dos participantes tiveram um envolvimento mais intenso em atividades sociais. Por outro lado, valores extremamente baixos, como zero e uma saída, também foram observados com frequência significativa (22,2%), sugerindo que uma parte considerável dos participantes optou por uma vida social mais contida no período analisado. Essa diversidade de respostas ressalta a variedade de estilos de vida e preferências sociais dentro da amostra considerada.

    ### EXEMPLO 6
    Entrada: Em uma saída, no total, quanto você costuma gastar no estabelecimento? Valores
    Acima de R$200,00 11
    Até R$50,00 7
    De R$100,00 até R$150,00 32
    De R$150,00 até R$200,00 11
    De R$50,00 até R$100,00 41
    Total geral 102
    Saída: A análise da tabela acima nos revela uma distribuição variada nos gastos dos frequentadores em estabelecimentos durante uma saída. A maioria dos entrevistados (41), representando 40,2%, gasta entre R$50,00 e R$100,00. Isso sugere que uma proporção significativa de consumidores prefere manter seus gastos em um nível moderado durante uma saída, optando por opções que se encaixam nessa faixa de preço. Em seguida, 32% dos entrevistados (32 participantes da amostra) relataram gastar entre R$100,00 e R$150,00, indicando que um número considerável de consumidores está disposto a gastar um pouco mais durante uma saída, optando por opções um pouco mais caras, mas ainda dentro de um limite razoável. Uma proporção menor de entrevistados, representando 10,8%, relatou gastar entre R$150,00 e R$200,00, enquanto a mesma porcentagem relatou gastos acima de R$200,00. Tal fato, revela que uma parcela menor dos frequentadores está disposta a gastar quantias mais substanciais durante uma saída, optando por opções mais caras ou indulgentes. Por fim, apenas 6,9% dos entrevistados (7 participantes) relataram gastar até R$50,00 durante uma saída. Isso sugere que uma minoria opta por manter seus gastos em um nível mais baixo durante essas ocasiões.

    ### EXEMPLO 7
    Entrada: O que é indispensável em um bar e/ou festa para você? Valores
    Música 23
    Bebida 12
    Ambiente (conforto/atendimento) 56
    Público 13
    Valor atrativo 6
    Saída: A análise da tabela revela que, para a maioria dos entrevistados, o aspecto mais indispensável em um bar e/ou festa é o ambiente, que engloba conforto e atendimento, representando 50,9% das preferências (56 entrevistados). Isso sugere que a qualidade do ambiente e a experiência geral oferecida pelo estabelecimento são aspectos críticos que influenciam a escolha dos frequentadores. A música também é considerada importante, com 20,9% dos entrevistados (23 participantes), destacando a importância da atmosfera sonora para criar o clima adequado e aumentar a experiência dos frequentadores. Ademais, o público foi mencionado por 13 entrevistados, totalizando 11,8%, como um aspecto indispensável, sugerindo que a interação social e a composição do público presente podem influenciar a experiência dos frequentadores em um estabelecimento. Em contrapartida, a bebida e o valor atrativo foram mencionados por uma proporção menor de entrevistados, com 10,9% e 5,5% respectivamente, como aspectos indispensáveis. Isso sugere que, embora sejam importantes, esses aspectos podem ser menos críticos na decisão de frequentar um bar e/ou festa em comparação com o ambiente, música e público.

    ### EXEMPLO 8
    Entrada: Ao escolher consumir algo saudável e inclusivo, o que mais te atrai no cardápio?
    Qtd. Repres.
    Variedade de opções 72 40,45%
    Ingredientes frescos e
    naturais 90 50,56%
    Sabor 60 33,71%
    Valor justo 106 59,55%
    Opções sem
    glúten/lactose/açúcar 44 24,72%
    Experiência 1 0,56%
    Poucas calorias 1 0,56%
    Saída:A amostra apresenta os principais fatores que atraem os consumidores a escolherem opções saudáveis e inclusivas no cardápio. O critério mais valorizado é o valor justo, citado por 106 respondentes, representando 59,55% da amostra. Em seguida, destaca-se a utilização de ingredientes frescos e naturais, com 90 menções que representam 50,56%, e a variedade de opções, apontada por 72 pessoas que são 40,45% do total. O sabor também possui relevância, sendo citado por 60 indivíduos (33,71%). Outro aspecto importante como opções sem glúten, lactose ou açúcar aparecem com 24,72%, enquanto experiência e poucas calorias foram pouco mencionadas, com apenas 0,56% cada. Esses dados indicam que os consumidores priorizam o equilíbrio entre um preço adequado e ingredientes naturais, além de uma tendência de diversidade de produtos.

    ### CASO ATUAL PARA ANALISAR
    Entrada: {dados_linha}
    Saída:
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro: {e}"

    
uploaded_file = st.file_uploader("Solte seu arquivo CSV aqui ", type=['csv'])

if uploaded_file and api_key:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        
        st.success("Arquivo carregado com sucesso!")
        st.write("Visualização dos dados:")
        st.dataframe(df.head(3), hide_index=True) 
        
        # 3. Escolher colunas
        usar_todas = st.checkbox("Selecionar todas as colunas")
        
        colunas_para_ler = st.multiselect(
            "Quais colunas a IA deve ler para criar a descrição?",
            options=df.columns,
            default=df.columns.tolist() if usar_todas else None,
            key=f"cols_{usar_todas}"
        )
        
        # 4. Botão de Processar
        if st.button("Gerar Descrições"):
            if not colunas_para_ler:
                st.error("Selecione pelo menos uma coluna para a IA ler.")
            elif len(colunas_para_ler) > 20:
                st.error(f"⚠️ Limite excedido: Você selecionou {len(colunas_para_ler)} colunas. O máximo permitido é 20 por vez.")
            else:
                client = genai.Client(api_key=api_key)
                
                # Barra de progresso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                descricoes = []
                total_colunas = len(colunas_para_ler)
                
                
                # Loop por cada coluna selecionada
                for index, col in enumerate(colunas_para_ler):
                    # Calcula a contagem e porcentagem usando pandas
                    contagem = df[col].value_counts()
                    porcentagens = df[col].value_counts(normalize=True) * 100
                    
                    # Formata os dados no padrão dos exemplos do prompt
                    linhas_texto = [f"{col} Qtd. Repres."]
                    for valor, qtd in contagem.items():
                        rep = porcentagens[valor]
                        # Substitui ponto por vírgula para o formato de porcentagem em PT-BR
                        linhas_texto.append(f"{valor} {qtd} {rep:.2f}%".replace('.', ','))
                    
                    linhas_texto.append(f"Total geral {contagem.sum()} 100,00%")
                    texto_dados = "\n".join(linhas_texto)
                    
                    # Chama a IA
                    resultado = gerar_descricao_row(texto_dados, client, len(df))
                    descricoes.append(resultado)
                    
                    # Atualiza barra
                    progress_bar.progress((index + 1) / total_colunas)
                    status_text.text(f"Processando coluna {index + 1} de {total_colunas}...")
                    
                    time.sleep(6.1)
                
                # Cria DataFrame com os resultados
                df_resultado = pd.DataFrame({"Coluna": colunas_para_ler, "Descricao_IA": descricoes})
                
                st.success("Processamento concluído!")
                
                # Mostra o resultado final
                st.dataframe(df_resultado, hide_index=True)
                
                # 5. Botão de Download
                # Converte para CSV para download
                csv = df_resultado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Baixar Planilha Pronta (CSV)",
                    data=csv,
                    file_name="relatorio_gerado.csv",
                    mime="text/csv",
                )
                
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")

elif uploaded_file and not api_key:
    st.warning("Por favor, insira sua API Key na barra lateral.")