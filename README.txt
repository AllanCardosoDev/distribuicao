README.txt
===============================================================================

SISTEMA DE LOTAÇÃO DE MILITARES - CFSD BM 2025

Este é um aplicativo Streamlit desenvolvido para gerenciar o processo de lotação de militares do CFSD BM 2025 (Corpo de Bombeiros Militar) no estado do Amazonas. O sistema permite que os militares escolham suas cidades de lotação de acordo com sua classificação geral, garantindo que as vagas sejam preenchidas de forma ordenada e que cada vaga fique indisponível após ser escolhida.

-------------------------------------------------------------------------------
FUNCIONALIDADES:
-------------------------------------------------------------------------------

*   **Classificação Geral:** Exibe a lista de militares com suas classificações e médias, carregada a partir de uma planilha Excel.
*   **Vagas por Cidade:** Apresenta as cidades de lotação disponíveis no Amazonas (Manaus, Parintins, Itacoatiara, Manacapuru, Coari, Tefé, Humaitá, Tabatinga, Presidente Figueiredo, Rio Preto da Eva) e o número de vagas em cada uma.
*   **Escolha Ordenada:** Permite que os militares (ou o operador do sistema) selecionem uma cidade de lotação, seguindo a ordem de classificação.
*   **Atualização de Vagas:** Automaticamente reduz o número de vagas disponíveis na cidade escolhida.
*   **Registro de Lotações:** Mantém um registro das escolhas de lotação já realizadas.
*   **Reiniciar Sistema:** Opção para resetar o sistema, restaurando as vagas e as escolhas para o estado inicial.

-------------------------------------------------------------------------------
COMO UTILIZAR:
-------------------------------------------------------------------------------

1.  **Pré-requisitos:**
    *   Python 3.x instalado.
    *   Bibliotecas Python: `streamlit`, `pandas`, `openpyxl`.
        Instale-as usando pip:
        `pip install streamlit pandas openpyxl`

2.  **Estrutura de Arquivos:**
    *   Salve o código Python do aplicativo (por exemplo, `distribuicao.py`) em uma pasta.
    *   Coloque o arquivo da planilha de classificação dos militares, nomeado como `NOTAS.xlsx`, na *mesma pasta* que o script Python.

3.  **Executar o Aplicativo:**
    *   Abra o terminal ou prompt de comando.
    *   Navegue até a pasta onde você salvou os arquivos.
    *   Execute o comando:
        `streamlit run distribuicao.py`
    *   O aplicativo será aberto automaticamente no seu navegador web.

4.  **Interação:**
    *   Acompanhe a "Classificação Geral dos Militares" e as "Vagas Disponíveis por Cidade".
    *   Na seção "É a vez de:", o militar atual na fila será exibido.
    *   Selecione a "Cidade de lotação" desejada no menu suspenso. Apenas cidades com vagas disponíveis serão mostradas.
    *   Clique em "Confirmar Lotação para [Nome do Militar]" para registrar a escolha.
    *   O sistema avançará automaticamente para o próximo militar.
    *   As "Lotações Confirmadas" serão exibidas abaixo.
    *   Para reiniciar o processo, clique em "Reiniciar Sistema de Lotação".

-------------------------------------------------------------------------------
ESTRUTURA DA PLANILHA (NOTAS.xlsx):
-------------------------------------------------------------------------------

O sistema espera que a planilha `NOTAS.xlsx` contenha os dados de classificação na primeira aba (sheet_name=0), com um cabeçalho que inclui as seguintes colunas, a partir da linha onde "CLASSIF" é encontrado:

*   **CLASSIF:** Posição do militar na classificação (ex: "1º LUGAR").
*   **NOME COMPLETO:** Nome completo do militar.
*   **SOMA DAS MÉDIAS:** Soma das médias das disciplinas.
*   **PESOS:** Pesos utilizados no cálculo.
*   **MÉDIA 2 CASAS DECIMAIS:** Média final com duas casas decimais.
*   **MED 3 CASAS:** Média final com três casas decimais (critério de desempate).
*   **DATA DE NASCIMENTO:** Data de nascimento (critério de desempate).

O script está configurado para identificar o cabeçalho automaticamente, mesmo com as linhas de informações adicionais acima dos nomes das colunas.

-------------------------------------------------------------------------------
CONTATO:
-------------------------------------------------------------------------------

Para dúvidas ou sugestões, entre em contato com [Seu Nome/Departamento].

===============================================================================
