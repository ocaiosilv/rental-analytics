##  Projeto de Estudo: Pipeline de Dados 

###  Objetivo

Este é um projeto simples que foi usado para explorar mais como uma pipeline funciona, dando introdução a
 **Coleta e Limpeza de Dados** (Web Scraping)
 **Análise e Visualização** (EDA) e
 **Aplicação de algum modelo de predição ainda que simples**.
 
Embora o modelo de predição tenha tido resultados limitados, o projeto foi importante para explorar o fluxo de trabalho e aprender bibliotecas essenciais como **Pandas, Matplotlib e Scikit-learn**.

###  Como Rodar

1.  **Instale as dependências:**
    ```bash
    pip install pandas matplotlib seaborn scikit-learn cloudscraper beautifulsoup4
    ```
2.  **Execute a coleta de dados:**
    ```bash
    python scrapping.py
    ```
3.  **Explore a análise:**
    Abra e execute os notebooks (`DataAnalysis.ipynb` e `machinelearn.ipnyb`).

###  Arquivos
* `scrapping.py`: Coletor de dados.
* `DataAnalysis.ipynb`: Análise Exploratória e Visualização.
* `machinelearn.ipnyb`: Aplicação do modelo de Regressão Linear.


### Considerações gerais
De maneira geral, o projeto se demonstrou bem útil para explorar o conceito de pipeline e relativo a manutenção/refactor de código no github, apesar do seu desempenho não ter sido exatamente relevante devido a natureza dos dados coletados ( os preços dos alugueis não seguiam um padrão, mas sim a avaliação individual do proprietario) e a falta de dados mais relevantes para esse levantamento como proximidade a pontos de interesse.
