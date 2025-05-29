=================================================
Amazon Best-Sellers Market Intelligence Tool
=================================================

OVERVIEW
--------
Gain a decisive competitive edge for your e-commerce business by automating competitor and market analysis on Amazon. This market intelligence tool is designed for store owners, analysts, and marketers who need accurate, actionable data to make strategic decisions. It automates the tedious task of data collection from Amazon's Best-Sellers pages, saving you hours of manual work. This version is optimized for a balance of reliability and improved processing speed.

HOW IT WORKS: A ROBUST TWO-STAGE PROCESS
-----------------------------------------
This tool uses a refined two-stage process for data extraction:

Stage 1: Main Page Analysis (with Manual CAPTCHA Assistance & Pagination)
1. A Firefox browser window will open automatically, navigating to the Amazon Best-Sellers page you've configured.
2. The script will prompt you in the terminal to manually solve any CAPTCHA challenges presented in the browser. This human-in-the-loop step is crucial for bypassing Amazon's primary defenses.
3. Once the page is loaded, the tool extracts links for best-selling products.
4. Pagination: The script navigates through "Next Page" links to collect more product links, up to `MAX_PRODUCTS_TO_FETCH` or until no more pages are found (respecting `MAX_PAGES_TO_SCRAPE`).

Stage 2: Individual Product Extraction (Headless, Sequential & Optimized)
1. For each unique product link, a separate, invisible (headless) Firefox browser instance is launched.
2. To maintain stability, products are processed ONE BY ONE (sequentially - `MAX_WORKERS_STAGE_2 = 1`).
3. Key data (Title, Price, URL) is extracted. An optimized timeout (30 seconds via `WebDriverWait`) is used for the product title to load, balancing speed with success on most pages.
4. An optimized small random delay (0.5-1.0 seconds via `time.sleep`) is introduced between processing each product.
5. This stage also uses your existing Firefox profile (if found) for consistency.
6. If a product page fails (e.g., timeout), an HTML snapshot is saved for debugging.

KEY FEATURES
------------
* Reliable Data Extraction: Two-stage process with manual CAPTCHA solving and stable, sequential Stage 2 processing.
* Pagination Support: Collects products from multiple pages of best-seller lists.
* Uses Your Firefox Profile: Can utilize your existing Firefox profile, aiding in appearing as a regular user.
* Multi-Marketplace Support: Analyze any Amazon marketplace by changing `AMAZON_BEST_SELLERS_URL`.
* Configurable Limits: Control `MAX_PRODUCTS_TO_FETCH` and `MAX_PAGES_TO_SCRAPE`.
* Image Loading Disabled: `DISABLE_IMAGES_SELENIUM = True` by default for faster page loads.
* Dual-Format Reporting:
    * CSV Output: A complete log of all attempted products with 'Status', title, price, and URL.
    * PDF Output: A clean PDF report with successfully extracted products, now including Title, Price, and **Direct Product URL**.
* Debug HTML Files: Saves HTML of pages where data extraction fails.

DATA POINTS COLLECTED
---------------------
For each successfully processed product:
* Product Title
* Current Price (formatted for the correct currency)
* Direct URL to the Product Page

GETTING STARTED (QUICK START GUIDE)
-----------------------------------

Prerequisites:
* Python 3.8+ installed.
* Mozilla Firefox browser installed.
* Geckodriver: Download the `geckodriver` compatible with your Firefox version (e.g., v0.34.0 for Windows 64-bit from https://github.com/mozilla/geckodriver/releases). Extract and place `geckodriver.exe` in the SAME FOLDER as your Python script.

Installation (Python Libraries):
Open your terminal (PowerShell, CMD, etc.) and run:
`pip install pandas beautifulsoup4 selenium fpdf2`

(Or use `pip install -r requirements.txt` if you have one with these contents:
pandas
beautifulsoup4
selenium
fpdf2
)

Configuration:
Open your Python script file in a text editor. Settings are at the top:

* `CSV_OUTPUT_FILE`: Default 'historico_precos_BR_auto.csv'.
* `PDF_OUTPUT_FILE`: Default 'Relatorio_Mais_Vendidos_BR_auto.pdf'.
* `AMAZON_BEST_SELLERS_URL`: **CRITICAL!** Set this to your target Amazon Best-Sellers category page.
* `MAX_PRODUCTS_TO_FETCH`: Max products to collect. Default: 100.
* `MAX_PAGES_TO_SCRAPE`: Safety limit for pagination. Default: 10.
* `MAX_WORKERS_STAGE_2`: Number of parallel workers for Stage 2. **Set to 1 for best stability (current setting)**.
* `GECKODRIVER_PATH`: Default `"geckodriver.exe"`.
* `DISABLE_IMAGES_SELENIUM`: `True` to disable images (faster), `False` to load. Default: `True`.

Example `AMAZON_BEST_SELLERS_URL`:
* Electronics in Brazil: `"https://www.amazon.com.br/gp/bestsellers/electronics/"`
* Books in the US: `"https://www.amazon.com/gp/bestsellers/books/"`

Execution:
1. Ensure `geckodriver.exe` is in the script's folder.
2. Open your terminal.
3. Navigate to your script's directory, e.g.:
   `cd "C:\Users\Administrador\Desktop\PROJETO ESPECIALIS E-COMMERCE"`
4. Run the script:
   `python your_script_name.py`
   (Replace `your_script_name.py` with your file's actual name)

What to Expect During Execution:
1. A Firefox window opens.
2. The terminal will prompt you to solve any CAPTCHA in the browser.
3. After CAPTCHA (if any), Stage 1 (link collection with pagination) proceeds.
4. Firefox window closes. Stage 2 (product data extraction) begins, printing progress.
5. `.csv` and `.pdf` reports are generated in the project folder.

OUTPUT FILES
------------
* **[Configured CSV Name].csv**: Logs all attempted products with Timestamp, Title, Price, URL, and Status.
* **[Configured PDF Name].pdf**: Formatted report of successfully extracted products, including Title, Price, and URL.

IMPORTANT NOTES / TROUBLESHOOTING
---------------------------------
* **Geckodriver Placement:** Essential for the script to run.
* **Manual CAPTCHA:** Your intervention in Stage 1 is key.
* **Execution Time:** This version balances reliability with improved speed (30s timeout per product, shorter delays). If timeouts occur, increasing the 30s `WebDriverWait` in `process_one_product` (e.g., to 35s or 40s) might be needed for very slow pages, which would increase overall time but improve success rate.
* **Amazon Website Changes:** Amazon's layout can change, potentially requiring updates to CSS selectors in the code.
* **Debug HTML Files:** Useful for diagnosing failures on specific product pages.

TECHNOLOGIES USED
-----------------
* Python 3
* Selenium (with Firefox/Geckodriver)
* BeautifulSoup4
* Pandas
* FPDF2 (for PDF generation)

LICENSE
-------
(Consider adding: This project is licensed under the MIT License - see the LICENSE.md file for details)

DISCLAIMER
----------
This tool is for analytical and educational purposes. Use responsibly and be mindful of Amazon's terms of service. The developers are not responsible for any misuse or for actions taken by Amazon due to its use.

====================================================
Ferramenta de Inteligência de Mercado para Mais Vendidos da Amazon
====================================================

VISÃO GERAL
-----------
Obtenha uma vantagem competitiva decisiva para o seu negócio de e-commerce, automatizando a análise de concorrentes e de mercado na Amazon. Esta ferramenta de inteligência de mercado é projetada para proprietários de lojas, analistas e profissionais de marketing que precisam de dados precisos e acionáveis para tomar decisões estratégicas. Ela automatiza a tediosa tarefa de coleta de dados das páginas de "Mais Vendidos" da Amazon, economizando horas de trabalho manual. Esta versão é otimizada para um equilíbrio entre confiabilidade e velocidade de processamento aprimorada.

COMO FUNCIONA: UM PROCESSO ROBUSTO EM DUAS ETAPAS
-------------------------------------------------
Esta ferramenta utiliza um processo refinado em duas etapas para extração de dados:

Etapa 1: Análise da Página Principal (com Assistência Manual para CAPTCHA e Paginação)
1. Uma janela do navegador Firefox será aberta automaticamente, navegando para a página de "Mais Vendidos" da Amazon que você configurou.
2. O script exibirá uma mensagem no terminal, aguardando que VOCÊ resolva manualmente quaisquer desafios CAPTCHA apresentados no navegador. Este passo de intervenção humana é crucial.
3. Após a página ser carregada, a ferramenta extrai os links dos produtos mais vendidos.
4. Paginação: O script navega pelas páginas "Próxima página" para coletar mais links, até o limite `MAX_PRODUCTS_TO_FETCH` ou até não haver mais páginas (respeitando `MAX_PAGES_TO_SCRAPE`).

Etapa 2: Extração Individual de Produtos (Headless, Sequencial e Otimizado)
1. Para cada link de produto único, uma instância separada e invisível ("headless") do Firefox é iniciada.
2. Para manter a estabilidade, os produtos são processados UM POR UM (sequencialmente - `MAX_WORKERS_STAGE_2 = 1`).
3. Dados chave (Título, Preço, URL) são extraídos. Um timeout otimizado (30 segundos via `WebDriverWait`) é usado para o título do produto carregar, equilibrando velocidade e sucesso na maioria das páginas.
4. Um pequeno atraso aleatório otimizado (0.5-1.0 segundos via `time.sleep`) é introduzido entre o processamento de cada produto.
5. Esta etapa também utiliza seu perfil existente do Firefox (se encontrado) para consistência.
6. Se uma página de produto falhar (ex: timeout), um instantâneo HTML é salvo para depuração.

PRINCIPAIS CARACTERÍSTICAS
--------------------------
* Extração de Dados Confiável: Processo de duas etapas com CAPTCHA manual e Etapa 2 sequencial estável.
* Suporte à Paginação: Coleta produtos de múltiplas páginas.
* Usa Seu Perfil do Firefox: Pode utilizar seu perfil existente, ajudando a parecer um usuário regular.
* Suporte Multi-Marketplace: Analise qualquer Amazon alterando `AMAZON_BEST_SELLERS_URL`.
* Limites Configuráveis: Controle `MAX_PRODUCTS_TO_FETCH` e `MAX_PAGES_TO_SCRAPE`.
* Opção para Desabilitar Imagens: `DISABLE_IMAGES_SELENIUM = True` por padrão para carregamento mais rápido.
* Relatórios em Duplo Formato:
    * Saída CSV: Log completo de todos os produtos tentados com 'Status', título, preço e URL.
    * Saída PDF: Relatório PDF limpo com produtos extraídos com sucesso, agora incluindo Título, Preço e **URL Direta do Produto**.
* Arquivos HTML para Debug: Salva HTML de páginas onde a extração falha.

PONTOS DE DADOS COLETADOS
------------------------
Para cada produto processado com sucesso:
* Título do Produto
* Preço Atual (formatado para a moeda correta)
* URL Direta para a Página do Produto

COMO COMEÇAR (GUIA RÁPIDO)
---------------------------

Pré-requisitos:
* Python 3.8+ instalado.
* Navegador Mozilla Firefox instalado.
* Geckodriver: Baixe o `geckodriver` compatível com sua versão do Firefox (ex: v0.34.0 para Windows 64-bit de https://github.com/mozilla/geckodriver/releases). Extraia e coloque `geckodriver.exe` na MESMA PASTA do seu script Python.

Instalação (Bibliotecas Python):
Abra seu terminal (PowerShell, CMD, etc.) e execute:
`pip install pandas beautifulsoup4 selenium fpdf2`

(Ou use `pip install -r requirements.txt` se você tiver um com estes conteúdos:
pandas
beautifulsoup4
selenium
fpdf2
)

Configuração:
Abra seu arquivo de script Python em um editor de texto. As configurações estão no topo:

* `CSV_OUTPUT_FILE`: Padrão 'historico_precos_BR_auto.csv'.
* `PDF_OUTPUT_FILE`: Padrão 'Relatorio_Mais_Vendidos_BR_auto.pdf'.
* `AMAZON_BEST_SELLERS_URL`: **CRÍTICO!** Defina para a página da categoria de "Mais Vendidos" da Amazon desejada.
* `MAX_PRODUCTS_TO_FETCH`: Máximo de produtos a coletar. Padrão: 100.
* `MAX_PAGES_TO_SCRAPE`: Limite de segurança para paginação. Padrão: 10.
* `MAX_WORKERS_STAGE_2`: Workers paralelos para Etapa 2. **Configurado como 1 para melhor estabilidade (configuração atual)**.
* `GECKODRIVER_PATH`: Padrão `"geckodriver.exe"`.
* `DISABLE_IMAGES_SELENIUM`: `True` para desabilitar imagens (mais rápido), `False` para carregar. Padrão: `True`.

Exemplo de `AMAZON_BEST_SELLERS_URL`:
* Eletrônicos no Brasil: `"https://www.amazon.com.br/gp/bestsellers/electronics/"`
* Livros nos EUA: `"https://www.amazon.com/gp/bestsellers/books/"`

Execução:
1. Certifique-se de que `geckodriver.exe` está na pasta do script.
2. Abra seu terminal.
3. Navegue até o diretório do seu script, ex:
   `cd "C:\Users\Administrador\Desktop\PROJETO ESPECIALIS E-COMMERCE"`
4. Execute o script:
   `python seu_nome_de_script.py`
   (Substitua `seu_nome_de_script.py` pelo nome real do seu arquivo)

O que Esperar Durante a Execução:
1. Uma janela do Firefox abre.
2. O terminal solicitará que você resolva qualquer CAPTCHA no navegador.
3. Após o CAPTCHA (se houver), a Etapa 1 (coleta de links com paginação) prossegue.
4. A janela do Firefox fecha. A Etapa 2 (extração de dados do produto) começa, imprimindo o progresso.
5. Relatórios `.csv` e `.pdf` são gerados na pasta do projeto.

ARQUIVOS DE SAÍDA
-----------------
* **[NomeConfiguradoCSV].csv**: Registra todos os produtos tentados com Timestamp, Título, Preço, URL e Status.
* **[NomeConfiguradoPDF].pdf**: Relatório formatado dos produtos extraídos com sucesso, incluindo Título, Preço e URL.

NOTAS IMPORTANTES / SOLUÇÃO DE PROBLEMAS
---------------------------------------
* **Localização do Geckodriver:** Essencial para o script funcionar.
* **CAPTCHA Manual:** Sua intervenção na Etapa 1 é chave.
* **Tempo de Execução:** Esta versão equilibra confiabilidade com velocidade aprimorada (timeout de 30s por produto, atrasos curtos). Se ocorrerem timeouts, aumentar o `WebDriverWait` de 30s em `process_one_product` (ex: para 35s ou 40s) pode ser necessário para páginas muito lentas, o que aumentaria o tempo total mas melhoraria a taxa de sucesso.
* **Mudanças no Site da Amazon:** O layout da Amazon pode mudar, potencialmente exigindo atualizações nos seletores CSS no código.
* **Arquivos HTML de Debug:** Úteis para diagnosticar falhas em páginas específicas de produtos.

TECNOLOGIAS UTILIZADAS
----------------------
* Python 3
* Selenium (com Firefox/Geckodriver)
* BeautifulSoup4
* Pandas
* FPDF2 (para geração de PDF)

LICENÇA
-------
(Considere adicionar: Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE.md para detalhes)

AVISO LEGAL
-----------
Esta ferramenta é para fins analíticos e educacionais. Use com responsabilidade e esteja ciente dos termos de serviço da Amazon. Os desenvolvedores não são responsáveis por qualquer mau uso ou por ações tomadas pela Amazon devido ao seu uso.
