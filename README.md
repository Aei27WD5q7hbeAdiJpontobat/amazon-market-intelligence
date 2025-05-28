________________
Amazon Best-Sellers Market Intelligence Tool
Stop Guessing, Start Winning. Get the decisive competitive edge your e-commerce business needs by automating competitor analysis on Amazon.
This powerful market intelligence tool is designed for store owners, analysts, and marketers who need accurate, actionable data to make strategic decisions. It automates the tedious task of data collection, saving you hours of manual work so you can focus on what truly matters: growing your business.
How It Works: A Robust Two-Stage Process
This tool uses a sophisticated two-stage process to ensure the highest possible success rate for data extraction:
1. Stage 1: Main Page Analysis (with Manual Helper)
   * A Firefox browser window will open automatically, navigating to the Amazon Best-Sellers page you configured.
   * The script will wait for you to solve any CAPTCHA challenges manually. This human-in-the-loop step is crucial for bypassing Amazon's primary defenses.
   * Once the page is loaded, the tool extracts the links for the top 50 best-selling products.
2. Stage 2: Individual Product Extraction (Headless)
   * For each link found, the script launches a separate, invisible (headless) browser instance.
   * It carefully extracts the key data from each product page, one by one, with a random delay between requests to be respectful to Amazon's servers.
Key Features
* Reliable Data Extraction: The two-stage process with manual CAPTCHA solving drastically increases the reliability of the data collection.
* Uses Your Firefox Profile: The script can use your existing Firefox profile, leveraging your cookies and session data to appear as a regular user, which further reduces blocks.
* Multi-Marketplace Support: Analyze any Amazon marketplace (e.g., .com, .co.uk, .de, .com.br) by simply changing the URL in the script's configuration area.
* Dual-Format Reporting:
   1. historico_precos_BR_auto.csv: A complete CSV log of all products processed, including those that failed, for full transparency and debugging.
   2. Relatorio_Mais_Vendidos_BR_auto.pdf: A clean, professional PDF report containing only the successfully extracted products, perfect for quick reviews and sharing.
Data Points Collected
For each successfully processed product, the tool extracts the following essential data:
* Product Title
* Current Price (formatted for the correct currency, R$ or $)
* Direct URL to the Product Page
________________
Getting Started (Quick Start Guide)
Follow these steps to get the tool running in minutes.
1. Prerequisites
* You must have Python 3.8+ installed.
* You must have the Mozilla Firefox browser installed.
* Download the geckodriver compatible with your Firefox version. Place the geckodriver.exe file in the same folder as the amazon_tracker_auto.py script.
2. Installation
Open your terminal or command prompt and install the required Python libraries:


Bash




pip install pandas beautifulsoup4 selenium fpdf

3. Configuration
This is the most important step. Open the amazon_tracker_auto.py file in a text editor. All settings are at the top of the file:
* AMAZON_BEST_SELLERS_URL: Change this URL to the Amazon Best-Sellers category page you want to analyze.
* CSV_OUTPUT_FILE / PDF_OUTPUT_FILE: You can change the default names of the output files here if you wish.
Example AMAZON_BEST_SELLERS_URL settings:
* For Electronics in Brazil: "https://www.amazon.com.br/gp/bestsellers/electronics/"
* For Books in the US: "https://www.amazon.com/gp/bestsellers/books/"
4. Execution
With everything configured, run the script from your terminal:


Bash




python amazon_tracker_auto.py

What to expect:
1. A Firefox window will pop up.
2. Check your terminal. It will prompt you to solve any CAPTCHA in the browser window.
3. Once you solve the CAPTCHA (if any), the script will proceed automatically.
4. When it's finished, you will find the .csv and .pdf report files in the project folder.
________________
Technologies Used
* Python
* Selenium (with Firefox/Geckodriver)
* BeautifulSoup4
* Pandas
* FPDF
