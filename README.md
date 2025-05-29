=================================================
Amazon Best-Sellers Market Intelligence Tool
=================================================

OVERVIEW
--------
Get a decisive competitive edge for your e-commerce business by automating competitor and market analysis on Amazon. This market intelligence tool is designed for store owners, analysts, and marketers who need accurate, actionable data to make strategic decisions. It automates the tedious task of data collection from Amazon's Best-Sellers pages, saving you hours of manual work so you can focus on what truly matters: growing your business. This version prioritizes reliability and comprehensive data extraction.

HOW IT WORKS: A ROBUST TWO-STAGE PROCESS
-----------------------------------------
This tool uses a refined two-stage process to ensure the highest possible success rate for data extraction:

Stage 1: Main Page Analysis (with Manual CAPTCHA Assistance & Pagination)
1. A Firefox browser window will open automatically, navigating to the Amazon Best-Sellers page you've configured in the script.
2. The script will print a message in the terminal, waiting for YOU to manually solve any CAPTCHA challenges that Amazon might present in the browser window. This human-in-the-loop step is crucial for bypassing Amazon's primary defenses.
3. Once the page (and any CAPTCHA) is handled, the tool extracts the links for the best-selling products.
4. Pagination: The script will then attempt to navigate to subsequent "Next Page" links to collect more product links, up to the `MAX_PRODUCTS_TO_FETCH` limit or until no more pages are found (whichever comes first, also respecting a `MAX_PAGES_TO_SCRAPE` safety limit).

Stage 2: Individual Product Extraction (Headless, Sequential & Stable)
1. For each unique product link found in Stage 1, the script launches a separate, invisible (headless) Firefox browser instance.
2. To ensure maximum stability and avoid overloading the Amazon servers or your system, products are processed ONE BY ONE (sequentially).
3. It carefully extracts key data (Title, Price, URL) from each product page. A generous timeout (40 seconds) is used to wait for the product title to load, increasing the chance of successful extraction on slower pages.
4. A small random delay is introduced between processing each product.
5. Like Stage 1, this stage can also leverage your existing Firefox profile (if found) for consistency, which is safe in sequential mode.
6. If a product page fails to load its title within the timeout, or if an error occurs, the script logs the failure and saves an HTML snapshot of the page for debugging (e.g., `debug_timeout_PRODUCTID.html`).

KEY FEATURES
------------
* Reliable Data Extraction: The two-stage process with manual CAPTCHA solving and stable, sequential processing in Stage 2 (with generous timeouts) drastically increases the reliability and completeness of data collection.
* Pagination Support: Collects products from multiple pages of the best-seller lists for more comprehensive data.
* Uses Your Firefox Profile: The script can utilize your existing Firefox profile (if found), leveraging cookies and session data, which can help in appearing as a regular user and potentially reduce CAPTCHA frequency.
* Multi-Marketplace Support: Analyze any Amazon marketplace (e.g., .com, .co.uk, .de, .com.br) by simply changing the `AMAZON_BEST_SELLERS_URL` in the script's configuration.
* Configurable Limits: Control the maximum number of products to fetch (`MAX_PRODUCTS_TO_FETCH`) and pages to scrape (`MAX_PAGES_TO_SCRAPE`).
* Image Loading Disable Option: `DISABLE_IMAGES_SELENIUM` is set to `True` by default to potentially speed up page loads during scraping.
* Dual-Format Reporting:
    * CSV Output (e.g., `historico_precos_BR_auto.csv`): A complete CSV log of all products the script attempted to process, including a 'Status' column (Success/Failure), full title, price, and URL, for transparency and debugging.
    * PDF Output (e.g., `Relatorio_Mais_Vendidos_BR_auto.pdf`): A clean, professional PDF report containing only the successfully extracted products (Title and Price), perfect for quick reviews and sharing.
* Debug HTML Files: Saves HTML content of pages where data extraction fails (e.g., due to timeout), aiding in troubleshooting.

DATA POINTS COLLECTED
---------------------
For each successfully processed product, the tool extracts:
* Product Title
* Current Price (formatted for the correct currency, e.g., R$ for Brazil)
* Direct URL to the Product Page

GETTING STARTED (QUICK START GUIDE)
-----------------------------------
Follow these steps to get the tool running:

Prerequisites:
* Python 3.8+ installed.
* Mozilla Firefox browser installed.
* Geckodriver: Download the `geckodriver` compatible with your Firefox version.
    * Official releases: https://github.com/mozilla/geckodriver/releases
    * For example, for Firefox v115 and Windows 64-bit, you might use geckodriver v0.34.0.
    * Extract the downloaded ZIP file.
    * IMPORTANT: Place the `geckodriver.exe` file in the SAME FOLDER as your Python script (e.g., `amazon_tracker_auto.py`).

Installation (Python Libraries):
Open your terminal (PowerShell, CMD, or Git Bash) and install the required Python libraries by running:
`pip install pandas beautifulsoup4 selenium fpdf`

Alternatively, if a `requirements.txt` file is provided with the project, you can run:
`pip install -r requirements.txt`
(You can create a `requirements.txt` file with the following content:
pandas
beautifulsoup4
selenium
fpdf
)

Configuration:
This is a crucial step. Open your Python script file (e.g., `amazon_tracker_auto.py`) in a text editor. All primary settings are at the top of the file:

* `CSV_OUTPUT_FILE`: Default 'historico_precos_BR_auto.csv'. You can change this.
* `PDF_OUTPUT_FILE`: Default 'Relatorio_Mais_Vendidos_BR_auto.pdf'. You can change this.
* `AMAZON_BEST_SELLERS_URL`: **VERY IMPORTANT!** Change this URL to the Amazon Best-Sellers category page you want to analyze.
* `MAX_PRODUCTS_TO_FETCH`: Maximum number of products to attempt to collect. Default: 100.
* `MAX_PAGES_TO_SCRAPE`: Safety limit for how many pages of best-sellers the script will try to navigate. Default: 10.
* `MAX_WORKERS_STAGE_2`: Number of parallel workers for Stage 2. **Set to 1 for maximum stability (current recommended setting)**. Increasing this has previously led to instability and crashes.
* `GECKODRIVER_PATH`: Should be `"geckodriver.exe"` if the file is in the same folder as the script.
* `DISABLE_IMAGES_SELENIUM`: Set to `True` to disable image loading (faster), or `False` to load images. Default: `True`.

Example `AMAZON_BEST_SELLERS_URL` settings:
* For Electronics in Brazil: `"https://www.amazon.com.br/gp/bestsellers/electronics/"`
* For Books in the US: `"https://www.amazon.com/gp/bestsellers/books/"`
* For Video Games in the UK: `"https://www.amazon.co.uk/gp/bestsellers/videogames/"`

Execution:
1. Ensure `geckodriver.exe` is in the same folder as your Python script.
2. Open your terminal (PowerShell, CMD, or Git Bash).
3. Navigate to the directory where your script is saved. For example:
   `cd "C:\Users\Administrador\Desktop\PROJETO ESPECIALIS E-COMMERCE"`
4. Run the script using:
   `python your_script_name.py`
   (Replace `your_script_name.py` with the actual name of your file, e.g., `amazon_tracker_auto.py`)

What to Expect During Execution:
1. A Firefox browser window will pop up and navigate to the Amazon URL.
2. Check your terminal. It will display messages. Crucially, it will pause and prompt you to:
   `>>> Se a página pedir um CAPTCHA, resolva-o MANUALMENTE para continuar. <<<`
3. Look at the Firefox window. If there's a CAPTCHA (the "type the characters" challenge), solve it in the browser.
4. Once the CAPTCHA is solved (or if none appeared), the script will detect the product list and proceed to Stage 1 (link collection with pagination).
5. After Stage 1, the Firefox window will close.
6. Stage 2 (individual product data extraction) will begin, with progress printed in the terminal. This stage uses headless (invisible) browsers.
7. When the script is finished, you will find the `.csv` and `.pdf` report files in the project folder.

OUTPUT FILES
------------
* **[Configured CSV Name].csv**: Contains all products for which data extraction was ATTEMPTED. Includes columns for Timestamp, Title (or error message if failed), Price, URL, and a Status ('Success' or 'Failure').
* **[Configured PDF Name].pdf**: A formatted report listing only the SUCCESSFULLY extracted products with their titles and prices.

IMPORTANT NOTES / TROUBLESHOOTING
---------------------------------
* **Geckodriver is Key:** The script will show a critical error if `geckodriver.exe` is not found in the same folder as the script. Double-check its placement.
* **Manual CAPTCHA:** Your intervention in Stage 1 for CAPTCHAs is essential for the script's success.
* **Execution Time:** This version of the script prioritizes reliability. With `MAX_WORKERS_STAGE_2 = 1` (sequential processing for individual products) and generous timeouts (40 seconds per product page in Stage 2), the script can take a while to run, especially if fetching many products or if many pages load slowly. This is a trade-off for achieving a high success rate.
* **Amazon Website Changes:** Amazon frequently updates its website structure. If the script suddenly stops working or fails to extract data, the CSS selectors used to find elements (like product links, titles, prices, or pagination buttons) might need to be updated in the Python code.
* **Debug HTML Files:** If the script reports `Timeout` or `Title not found` for specific products, it will attempt to save an HTML file (e.g., `debug_timeout_PRODUCTID.html`). These files can be opened in a browser to see what the script saw and help diagnose why it failed for that page.

TECHNOLOGIES USED
-----------------
* Python 3
* Selenium (with Firefox/Geckodriver)
* BeautifulSoup4
* Pandas
* FPDF (for PDF generation)

LICENSE
-------
(Consider adding a license if you plan to share this publicly, e.g., MIT License. If not, you can omit this section or state "Proprietary".)

Example:
This project is licensed under the MIT License - see the LICENSE.md file for details (if you create one).

DISCLAIMER
----------
This tool is for educational and analytical purposes. Please use responsibly and be mindful of Amazon's terms of service. The developers are not responsible for any misuse of this tool or for any actions taken by Amazon as a result of its use. Scraping websites can be resource-intensive; use with consideration.


====================================================
Ferramenta de Inteligência de Mercado para Mais Vendidos da Amazon
====================================================

VISÃO GERAL
-----------
Obtenha uma vantagem competitiva decisiva para o seu negócio de e-commerce, automatizando a análise de concorrentes e de mercado na Amazon. Esta ferramenta de inteligência de mercado é projetada para proprietários de lojas, analistas e profissionais de marketing que precisam de dados precisos e acionáveis para tomar decisões estratégicas. Ela automatiza a tediosa tarefa de coleta de dados das páginas de "Mais Vendidos" da Amazon, economizando horas de trabalho manual para que você possa focar no que realmente importa: o crescimento do seu negócio. Esta versão prioriza a confiabilidade e a extração abrangente de dados.

COMO FUNCIONA: UM PROCESSO ROBUSTO EM DUAS ETAPAS
-------------------------------------------------
Esta ferramenta utiliza um processo refinado em duas etapas para garantir a maior taxa de sucesso possível na extração de dados:

Etapa 1: Análise da Página Principal (com Assistência Manual para CAPTCHA e Paginação)
1. Uma janela do navegador Firefox será aberta automaticamente, navegando para a página de "Mais Vendidos" da Amazon que você configurou no script.
2. O script exibirá uma mensagem no terminal, aguardando que VOCÊ resolva manualmente quaisquer desafios CAPTCHA que a Amazon possa apresentar na janela do navegador. Este passo de intervenção humana é crucial para contornar as principais defesas da Amazon.
3. Uma vez que a página (e qualquer CAPTCHA) é processada, a ferramenta extrai os links dos produtos mais vendidos.
4. Paginação: O script tentará então navegar para as páginas subsequentes ("Próxima página") para coletar mais links de produtos, até o limite definido em `MAX_PRODUCTS_TO_FETCH` ou até não haver mais páginas (o que ocorrer primeiro, respeitando também um limite de segurança `MAX_PAGES_TO_SCRAPE`).

Etapa 2: Extração Individual de Produtos (Headless, Sequencial e Estável)
1. Para cada link de produto único encontrado na Etapa 1, o script inicia uma instância separada e invisível ("headless") do navegador Firefox.
2. Para garantir máxima estabilidade e evitar sobrecarregar os servidores da Amazon ou seu sistema, os produtos são processados UM POR UM (sequencialmente).
3. Ele extrai cuidadosamente os dados chave (Título, Preço, URL) de cada página de produto. Um tempo de espera generoso (40 segundos) é usado para aguardar o carregamento do título do produto, aumentando a chance de extração bem-sucedida em páginas mais lentas.
4. Um pequeno atraso aleatório é introduzido entre o processamento de cada produto.
5. Assim como a Etapa 1, esta etapa também pode utilizar seu perfil existente do Firefox (se encontrado) para consistência, o que é seguro no modo sequencial.
6. Se uma página de produto falhar ao carregar seu título dentro do tempo limite, ou se ocorrer um erro, o script registra a falha e salva um instantâneo HTML da página para depuração (ex: `debug_timeout_IDPRODUTO.html`).

PRINCIPAIS CARACTERÍSTICAS
--------------------------
* Extração de Dados Confiável: O processo de duas etapas com resolução manual de CAPTCHA e processamento sequencial estável na Etapa 2 (com timeouts generosos) aumenta drasticamente a confiabilidade e completude da coleta de dados.
* Suporte à Paginação: Coleta produtos de múltiplas páginas das listas de mais vendidos para dados mais abrangentes.
* Usa Seu Perfil do Firefox: O script pode utilizar seu perfil existente do Firefox (se encontrado), aproveitando cookies e dados de sessão, o que pode ajudar a parecer um usuário regular e potencialmente reduzir a frequência de CAPTCHAs.
* Suporte Multi-Marketplace: Analise qualquer marketplace da Amazon (ex: .com, .co.uk, .de, .com.br) simplesmente alterando a `AMAZON_BEST_SELLERS_URL` na área de configuração do script.
* Limites Configuráveis: Controle o número máximo de produtos a serem buscados (`MAX_PRODUCTS_TO_FETCH`) e de páginas a serem varridas (`MAX_PAGES_TO_SCRAPE`).
* Opção para Desabilitar Imagens: `DISABLE_IMAGES_SELENIUM` está configurado como `True` por padrão para potencialmente acelerar o carregamento das páginas durante a raspagem.
* Relatórios em Duplo Formato:
    * Saída CSV (ex: `historico_precos_BR_auto.csv`): Um log CSV completo de todos os produtos que o script tentou processar, incluindo uma coluna 'Status' (Sucesso/Falha), título completo, preço e URL, para transparência e depuração.
    * Saída PDF (ex: `Relatorio_Mais_Vendidos_BR_auto.pdf`): Um relatório PDF limpo e profissional contendo apenas os produtos extraídos com sucesso (Título e Preço), perfeito para revisões rápidas e compartilhamento.
* Arquivos HTML para Debug: Salva o conteúdo HTML de páginas onde a extração de dados falha (ex: devido a timeout), auxiliando na solução de problemas.

PONTOS DE DADOS COLETADOS
------------------------
Para cada produto processado com sucesso, a ferramenta extrai:
* Título do Produto
* Preço Atual (formatado para a moeda correta, ex: R$ para o Brasil)
* URL Direta para a Página do Produto

COMO COMEÇAR (GUIA RÁPIDO)
---------------------------
Siga estes passos para colocar a ferramenta em funcionamento:

Pré-requisitos:
* Python 3.8+ instalado.
* Navegador Mozilla Firefox instalado.
* Geckodriver: Baixe o `geckodriver` compatível com sua versão do Firefox.
    * Releases oficiais: https://github.com/mozilla/geckodriver/releases
    * Por exemplo, para Firefox v115 e Windows 64-bit, você pode usar o geckodriver v0.34.0.
    * Extraia o arquivo ZIP baixado.
    * IMPORTANTE: Coloque o arquivo `geckodriver.exe` na MESMA PASTA que o seu script Python (ex: `amazon_tracker_auto.py`).

Instalação (Bibliotecas Python):
Abra seu terminal (PowerShell, CMD ou Git Bash) e instale as bibliotecas Python necessárias executando:
`pip install pandas beautifulsoup4 selenium fpdf2` 
*(Nota: Usamos fpdf2 pois é o sucessor moderno do fpdf e inclui `fpdf.enums`)*

Alternativamente, se um arquivo `requirements.txt` for fornecido com o projeto, você pode executar:
`pip install -r requirements.txt`
(Você pode criar um arquivo `requirements.txt` com o seguinte conteúdo:
pandas
beautifulsoup4
selenium
fpdf2
)

Configuração:
Este é um passo crucial. Abra seu arquivo de script Python (ex: `amazon_tracker_auto.py`) em um editor de texto. Todas as configurações principais estão no topo do arquivo:

* `CSV_OUTPUT_FILE`: Padrão 'historico_precos_BR_auto.csv'. Você pode alterar.
* `PDF_OUTPUT_FILE`: Padrão 'Relatorio_Mais_Vendidos_BR_auto.pdf'. Você pode alterar.
* `AMAZON_BEST_SELLERS_URL`: **MUITO IMPORTANTE!** Altere esta URL para a página da categoria de "Mais Vendidos" da Amazon que você deseja analisar.
* `MAX_PRODUCTS_TO_FETCH`: Número máximo de produtos que o script tentará coletar. Padrão: 100.
* `MAX_PAGES_TO_SCRAPE`: Limite de segurança para quantas páginas de mais vendidos o script tentará navegar. Padrão: 10.
* `MAX_WORKERS_STAGE_2`: Número de workers paralelos para a Etapa 2. **Configurado como 1 para máxima estabilidade (configuração atual recomendada)**. Aumentar este valor demonstrou levar a instabilidade e travamentos.
* `GECKODRIVER_PATH`: Deve ser `"geckodriver.exe"` se o arquivo estiver na mesma pasta do script.
* `DISABLE_IMAGES_SELENIUM`: Configure como `True` para desabilitar o carregamento de imagens (mais rápido), ou `False` para carregar imagens. Padrão: `True`.

Exemplos de configurações de `AMAZON_BEST_SELLERS_URL`:
* Para Eletrônicos no Brasil: `"https://www.amazon.com.br/gp/bestsellers/electronics/"`
* Para Livros nos EUA: `"https://www.amazon.com/gp/bestsellers/books/"`
* Para Videogames no Reino Unido: `"https://www.amazon.co.uk/gp/bestsellers/videogames/"`

Execução:
1. Certifique-se de que o `geckodriver.exe` está na mesma pasta do seu script Python.
2. Abra seu terminal (PowerShell, CMD ou Git Bash).
3. Navegue até o diretório onde seu script está salvo. Por exemplo:
   `cd "C:\Users\Administrador\Desktop\PROJETO ESPECIALIS E-COMMERCE"`
4. Execute o script usando:
   `python seu_nome_de_script.py`
   (Substitua `seu_nome_de_script.py` pelo nome real do seu arquivo, ex: `amazon_tracker_auto.py`)

O que Esperar Durante a Execução:
1. Uma janela do navegador Firefox aparecerá e navegará para a URL da Amazon.
2. Verifique seu terminal. Ele exibirá mensagens. Crucialmente, ele pausará e solicitará que você:
   `>>> Se a página pedir um CAPTCHA, resolva-o MANUALMENTE para continuar. <<<`
3. Olhe para a janela do Firefox. Se houver um CAPTCHA (o desafio de "digite os caracteres"), resolva-o no navegador.
4. Após o CAPTCHA ser resolvido (ou se nenhum aparecer), o script detectará a lista de produtos e prosseguirá para a Etapa 1 (coleta de links com paginação).
5. Após a Etapa 1, a janela do Firefox fechará.
6. A Etapa 2 (extração individual de dados de produtos) começará, com o progresso impresso no terminal. Esta etapa usa navegadores invisíveis (headless).
7. Quando o script terminar, você encontrará os arquivos de relatório `.csv` e `.pdf` na pasta do projeto.

ARQUIVOS DE SAÍDA
-----------------
* **[NomeConfiguradoCSV].csv**: Contém todos os produtos para os quais a extração de dados foi TENTADA. Inclui colunas para Timestamp, Título (ou mensagem de erro se falhou), Preço, URL e um Status ('Sucesso' ou 'Falha').
* **[NomeConfiguradoPDF].pdf**: Um relatório formatado listando apenas os produtos EXTRAÍDOS COM SUCESSO com seus títulos e preços.

NOTAS IMPORTANTES / SOLUÇÃO DE PROBLEMAS
---------------------------------------
* **Geckodriver é Essencial:** O script mostrará um erro crítico se o `geckodriver.exe` não for encontrado na mesma pasta do script. Verifique novamente sua localização.
* **CAPTCHA Manual:** Sua intervenção na Etapa 1 para CAPTCHAs é fundamental para o sucesso do script.
* **Tempo de Execução:** Esta versão do script prioriza a confiabilidade. Com `MAX_WORKERS_STAGE_2 = 1` (processamento sequencial para produtos individuais) e timeouts generosos (40 segundos por página de produto na Etapa 2), o script pode levar um tempo para rodar, especialmente se buscando muitos produtos ou se muitas páginas carregarem lentamente. Esta é uma troca para alcançar uma alta taxa de sucesso.
* **Mudanças no Site da Amazon:** A Amazon frequentemente atualiza a estrutura do seu site. Se o script parar de funcionar subitamente ou falhar na extração de dados, os seletores CSS usados para encontrar elementos (como links de produtos, títulos, preços ou botões de paginação) podem precisar ser atualizados no código Python.
* **Arquivos HTML de Debug:** Se o script relatar `Timeout` ou `Title not found` para produtos específicos, ele tentará salvar um arquivo HTML (ex: `debug_timeout_IDPRODUTO.html`). Esses arquivos podem ser abertos em um navegador para ver o que o script visualizou e ajudar a diagnosticar por que falhou para aquela página.

TECNOLOGIAS UTILIZADAS
----------------------
* Python 3
* Selenium (com Firefox/Geckodriver)
* BeautifulSoup4
* Pandas
* FPDF2 (para geração de PDF)

LICENÇA
-------
(Considere adicionar uma licença se você planeja compartilhar isso publicamente, ex: Licença MIT. Se não, você pode omitir esta seção ou declarar "Proprietário".)

Exemplo:
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE.md para detalhes (se você criar um).

AVISO LEGAL
-----------
Esta ferramenta é para fins educacionais e analíticos. Por favor, use com responsabilidade e esteja ciente dos termos de serviço da Amazon. Os desenvolvedores não são responsáveis por qualquer mau uso desta ferramenta ou por quaisquer ações tomadas pela Amazon como resultado de seu uso. A raspagem de sites pode consumir muitos recursos; use com consideração.
