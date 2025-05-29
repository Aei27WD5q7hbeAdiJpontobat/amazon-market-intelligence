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
