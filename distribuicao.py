import streamlit as st
import pandas as pd

# Função para carregar os dados da planilha
@st.cache_data
def load_data(file_path):
    try:
        # Carrega a planilha inteira para inspecionar o cabeçalho
        # header=None para não tentar adivinhar o cabeçalho inicialmente
        df_raw = pd.read_excel(file_path, sheet_name=0, header=None)

        # Encontra a linha que contém 'CLASSIF' para usar como cabeçalho
        # Converte a primeira coluna para string para evitar erros com tipos mistos
        header_row_index = df_raw[df_raw.iloc[:, 0].astype(str).str.contains('CLASSIF', na=False)].index[0]

        # Agora, carrega a planilha novamente, usando a linha encontrada como cabeçalho
        # skiprows pula as linhas até o cabeçalho (inclusive a linha do cabeçalho - 1)
        df = pd.read_excel(file_path, sheet_name=0, skiprows=header_row_index)

        # Renomear colunas para facilitar o acesso e lidar com nomes duplicados/vazios
        # Baseado na estrutura da sua planilha, as colunas são:
        # CLASSIF, NOME COMPLETO, SOMA DAS MÉDIAS, PESOS, MÉDIA 2 CASAS DECIMAIS, MED 3 CASAS, DATA DE NASCIMENTO
        df.columns = ['CLASSIF', 'NOME COMPLETO', 'SOMA DAS MÉDIAS', 'PESOS',
                      'MÉDIA 2 CASAS DECIMAIS', 'MED 3 CASAS', 'DATA DE NASCIMENTO']

        # Remover linhas que não têm nome completo (geralmente linhas de cabeçalho ou rodapé indesejadas)
        df = df.dropna(subset=['NOME COMPLETO'])

        # Limpar a coluna 'CLASSIF' para ter apenas o número inteiro
        # Primeiro, converte para string para poder usar .split('º')
        df['CLASSIF'] = df['CLASSIF'].astype(str).apply(lambda x: int(x.split('º')[0]) if 'º' in x else x)
        # Converte para numérico, transformando erros em NaN
        df['CLASSIF'] = pd.to_numeric(df['CLASSIF'], errors='coerce')
        # Remove linhas onde a classificação não é um número válido
        df = df.dropna(subset=['CLASSIF'])
        # Converte para inteiro
        df['CLASSIF'] = df['CLASSIF'].astype(int)

        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        st.error("Verifique se o nome do arquivo está correto ('NOTAS.xlsx') e se o formato do cabeçalho da planilha está conforme o esperado.")
        return pd.DataFrame()

# Cidades de lotação no Amazonas e vagas iniciais
# Estas são sugestões baseadas em municípios com presença do CBMAM ou importância estratégica.
# Você pode ajustar os números conforme a necessidade real.
initial_vacancies = {
    "Manaus": 100,
    "Parintins": 10,
    "Itacoatiara": 8,
    "Manacapuru": 7,
    "Coari": 6,
    "Tefé": 5,
    "Humaitá": 4,
    "Tabatinga": 5,
    "Presidente Figueiredo": 5,
    "Rio Preto da Eva": 5,
}

def app():
    st.title("Sistema de Lotação de Militares - CFSD BM 2025")
    st.subheader("Escolha de Lotação por Classificação")

    # Carregar dados - AGORA APONTA PARA "NOTAS.xlsx"
    df = load_data("NOTAS.xlsx")

    if df.empty:
        st.warning("Não foi possível carregar os dados da planilha. Verifique o arquivo e o console para mais detalhes.")
        return

    # Inicializar estado da sessão para vagas e escolhas
    if 'vacancies' not in st.session_state:
        st.session_state.vacancies = initial_vacancies.copy()
    if 'choices' not in st.session_state:
        st.session_state.choices = {} # {nome_militar: cidade_escolhida}
    if 'current_militar_index' not in st.session_state:
        st.session_state.current_militar_index = 0

    st.write("---")

    # Exibir a lista de militares e suas classificações
    st.subheader("Classificação Geral dos Militares")
    st.dataframe(df[['CLASSIF', 'NOME COMPLETO', 'MÉDIA 2 CASAS DECIMAIS']].set_index('CLASSIF'))

    st.write("---")

    # Exibir vagas disponíveis
    st.subheader("Vagas Disponíveis por Cidade")
    vacancies_df = pd.DataFrame(st.session_state.vacancies.items(), columns=['Cidade', 'Vagas Disponíveis'])
    st.dataframe(vacancies_df.set_index('Cidade'))

    st.write("---")

    # Lógica de escolha
    if st.session_state.current_militar_index < len(df):
        current_militar = df.iloc[st.session_state.current_militar_index]
        militar_nome = current_militar['NOME COMPLETO']
        militar_classif = current_militar['CLASSIF']

        st.subheader(f"É a vez de: {militar_classif}º LUGAR - {militar_nome}")

        available_cities = {city: count for city, count in st.session_state.vacancies.items() if count > 0}

        if not available_cities:
            st.warning("Não há mais vagas disponíveis em nenhuma cidade.")
            st.session_state.current_militar_index = len(df) # Avança para o final
            return

        city_options = list(available_cities.keys())
        selected_city = st.selectbox("Escolha a cidade de lotação:", city_options, key=f"select_{militar_classif}")

        if st.button(f"Confirmar Lotação para {militar_nome}", key=f"confirm_button_{militar_classif}"):
            if selected_city:
                st.session_state.vacancies[selected_city] -= 1
                st.session_state.choices[militar_nome] = selected_city
                st.success(f"{militar_nome} lotado(a) em {selected_city}.")
                st.session_state.current_militar_index += 1
                st.experimental_rerun() # Recarrega para atualizar a interface
            else:
                st.warning("Por favor, selecione uma cidade.")
    else:
        st.success("Todos os militares fizeram suas escolhas de lotação!")

    st.write("---")

    # Exibir escolhas já feitas
    st.subheader("Lotações Confirmadas")
    if st.session_state.choices:
        choices_df = pd.DataFrame(st.session_state.choices.items(), columns=['Militar', 'Cidade de Lotação'])
        st.dataframe(choices_df)
    else:
        st.info("Nenhuma lotação foi confirmada ainda.")

    st.write("---")
    if st.button("Reiniciar Sistema de Lotação"):
        st.session_state.vacancies = initial_vacancies.copy()
        st.session_state.choices = {}
        st.session_state.current_militar_index = 0
        st.experimental_rerun()

if __name__ == "__main__":
    app()
