import pandas as pd
from datetime import datetime
import os
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF 
from fpdf.enums import XPos, YPos 
import glob 
import re 

# Importações do Selenium para Firefox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# --- CONFIGURAÇÃO ---
CSV_OUTPUT_FILE = 'historico_precos_BR_auto.csv' 
PDF_OUTPUT_FILE = 'Relatorio_Mais_Vendidos_BR_auto.pdf'
AMAZON_BEST_SELLERS_URL = "https://www.amazon.com.br/gp/bestsellers/electronics/"
MAX_PRODUCTS_TO_FETCH = 100 
MAX_PAGES_TO_SCRAPE = 10  

# --- MODO DE EXECUÇÃO DA ETAPA 2 (Processamento individual dos produtos) ---
# Mantendo em 1 para MÁXIMA ESTABILIDADE.
MAX_WORKERS_STAGE_2 = 1

# --- CAMINHO DO DRIVER (MÉTODO MANUAL) ---
GECKODRIVER_PATH = "geckodriver.exe" 
DISABLE_IMAGES_SELENIUM = True 

USER_AGENTS_FOR_SELENIUM = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

def get_profile_path(profile_name='default-release'):
    try:
        base_path = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
        if not os.path.exists(base_path): 
            print("AVISO: Diretório de perfis do Firefox não encontrado.")
            return None
        profile_directories = glob.glob(os.path.join(base_path, f'*.{profile_name}'))
        if not profile_directories:
            print(f"AVISO: Nenhum perfil do Firefox com nome '{profile_name}' foi encontrado.")
            return None
        profile_directory = profile_directories[0]
        print(f"Usando o perfil do Firefox encontrado em: {profile_directory}")
        return profile_directory
    except Exception as e:
        print(f"Não foi possível encontrar o perfil do Firefox: {e}")
        return None

FIREFOX_PROFILE_PATH = get_profile_path()

def setup_driver(is_headless=False, use_profile=True): 
    options = Options()
    if use_profile and FIREFOX_PROFILE_PATH: 
        options.add_argument("-profile")
        options.add_argument(FIREFOX_PROFILE_PATH)
    
    if is_headless:
        options.add_argument("-headless")
    options.set_preference("general.useragent.override", random.choice(USER_AGENTS_FOR_SELENIUM))
    
    if DISABLE_IMAGES_SELENIUM:
        options.set_preference("permissions.default.image", 2) 
        options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")

    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", True) 
    options.set_preference("network.http.pipelining", True)
    options.set_preference("network.http.proxy.pipelining", True)
    options.set_preference("network.http.pipelining.maxrequests", 8)
    options.set_preference("network.prefetch-next", False)
    
    service = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def encontrar_links_bestsellers_automatico():
    print(f"--- ETAPA 1 (SELENIUM/FIREFOX): Acessando {AMAZON_BEST_SELLERS_URL} ---")
    driver = None
    product_links = []
    try:
        driver = setup_driver(is_headless=False, use_profile=True) 
        print(f" -> Navegando para a página inicial dos Mais Vendidos...")
        driver.get(AMAZON_BEST_SELLERS_URL)
        
        print("\n>>> ATENÇÃO: Uma janela do Firefox foi aberta. <<<")
        print(">>> Se a página pedir um CAPTCHA, resolva-o MANUALMENTE para continuar.")
        print(">>> O script aguardará até que a lista de produtos seja encontrada (máx 2 minutos na primeira página)... <<<\n")
        
        page_count = 1
        
        while page_count <= MAX_PAGES_TO_SCRAPE and len(product_links) < MAX_PRODUCTS_TO_FETCH:
            print(f" -> Analisando página {page_count} (Coletados: {len(product_links)} de {MAX_PRODUCTS_TO_FETCH})...")
            wait_time = 120 if page_count == 1 else 30 
            try:
                WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[id^='p13n-asin-index-']"))
                )
            except TimeoutException:
                print(f" -> Tempo esgotado esperando produtos na página {page_count}. Pode ser o fim.")
                break
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_items_on_page = soup.select("div[id^='p13n-asin-index-']")
            if not product_items_on_page:
                print(f" -> Nenhum produto encontrado na página {page_count}.")
                break 
            current_url_base = "/".join(driver.current_url.split("/")[:3]) 
            new_links_found_on_this_page = 0
            for item in product_items_on_page:
                if len(product_links) >= MAX_PRODUCTS_TO_FETCH: break
                link_tag = item.select_one('a.a-link-normal[href*="/dp/"]')
                if link_tag and 'href' in link_tag.attrs:
                    href = link_tag['href'].split('/ref=')[0]
                    if href.startswith('/'): url_complete = current_url_base + href
                    else: url_complete = href
                    if url_complete not in product_links:
                        product_links.append(url_complete)
                        new_links_found_on_this_page +=1
            if len(product_links) >= MAX_PRODUCTS_TO_FETCH:
                print(f" -> Limite de {MAX_PRODUCTS_TO_FETCH} produtos atingido.")
                break
            if new_links_found_on_this_page == 0 and page_count > 1 :
                 print(f" -> Nenhum link novo encontrado na página {page_count}, assumindo fim da lista.")
                 break
            try:
                next_page_li_element = driver.find_element(By.CSS_SELECTOR, "ul.a-pagination li.a-last")
                if "a-disabled" in next_page_li_element.get_attribute("class"):
                    print(" -> Fim da paginação (botão 'Próximo' desabilitado).")
                    break
                next_page_link_element = next_page_li_element.find_element(By.TAG_NAME, "a")
                driver.execute_script("arguments[0].click();", next_page_link_element)
                page_count += 1
                print(f" -> Navegando para a página {page_count}...")
                time.sleep(random.uniform(3, 6)) 
            except NoSuchElementException:
                print(" -> Fim da paginação (elemento 'Próximo' não encontrado).")
                break
            except Exception as e_page:
                print(f" -> Erro na paginação: {type(e_page).__name__} - {e_page}")
                break
        
        print(f"--- {len(product_links)} links de produtos encontrados no total. ---")
        return product_links
    except Exception as e:
        print(f"Falha CRÍTICA na Etapa 1 (Selenium): {type(e).__name__} - {e}")
        if driver:
            with open("debug_etapa1_erro_critico.html", "w", encoding="utf-8") as f_debug:
                f_debug.write(driver.page_source)
            print("INFO: HTML da página de erro salvo.")
        return []
    finally:
        if driver:
            driver.quit()
            print(" -> Navegador da Etapa 1 fechado.")

def clean_price(price_text_input, domain_base):
    if not price_text_input: return "Unavailable"
    price_text = price_text_input.strip()
    if "indisponível" in price_text.lower(): return "Unavailable"
    cleaned_text = price_text.replace('R$', '').replace('$', '').strip()
    if "amazon.com.br" in domain_base: 
        cleaned_text = cleaned_text.replace('.', '').replace(',', '.')
    else:
        cleaned_text = cleaned_text.replace(',', '')
    match = re.search(r'(\d+\.?\d*)', cleaned_text)
    return match.group(1) if match else "Error: NotNumeric"

def process_one_product(url_info):
    url = url_info['url']
    base_domain = url_info['base_domain']
    driver = None
    safe_url_filename_part = url.split('/')[-1].split('?')[0].replace('%', '_') 
    if len(safe_url_filename_part) > 50: 
        safe_url_filename_part = safe_url_filename_part[:50]

    display_url = url[:70] + "..." if len(url) > 70 else url
    print(f" -> Processando: {display_url}") 

    try:
        driver = setup_driver(is_headless=True, use_profile=True) 
        driver.get(url)
        
        # Timeout ajustado para 30s
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "productTitle")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title_element = soup.find('span', id='productTitle')
        title = title_element.get_text(strip=True) if title_element else 'Title not found'
        price = 'Unavailable'
        currency_symbol = "R$" if "amazon.com.br" in base_domain else "$"

        if title != 'Title not found':
            price_element = soup.select_one('span.a-price.a-text-price span.a-offscreen, #corePrice_feature_div span.a-offscreen')
            if price_element:
                cleaned_price = clean_price(price_element.get_text(strip=True), base_domain)
                if "Error" not in cleaned_price: price = cleaned_price

        if title != 'Title not found':
            print(f"   [OK] Extraído: {title[:40]}... | Preço: {currency_symbol}{price}")
        else:
            print(f"   [FALHA] Título não encontrado para: {url}")
            with open(f"debug_titulo_nao_encontrado_{safe_url_filename_part}.html", "w", encoding="utf-8") as f_debug:
                f_debug.write(driver.page_source)
            print(f"   INFO: HTML da página de falha salvo.")
            
        return {'url': url, 'title': title, 'price': price}
    except TimeoutException: 
        print(f"   [FALHA] Timeout (30s) ao esperar pelo título em {url}")
        if driver:
            with open(f"debug_timeout_{safe_url_filename_part}.html", "w", encoding="utf-8") as f_debug:
                f_debug.write(driver.page_source)
            print(f"   INFO: HTML da página de timeout salvo.")
        return {'url': url, 'title': 'PROCESSING FAILED (TIMEOUT)', 'price': 'N/A'}
    except WebDriverException as e_wd:
        print(f"   [FALHA] WebDriverException ao processar {url}: {type(e_wd).__name__} - {str(e_wd)[:100]}") 
        return {'url': url, 'title': f'PROCESSING FAILED ({type(e_wd).__name__})', 'price': 'N/A'}
    except Exception as e:
        print(f"   [FALHA] Erro desconhecido ao processar {url}: {type(e).__name__}")
        if driver:
            try:
                with open(f"debug_erro_geral_{safe_url_filename_part}.html", "w", encoding="utf-8") as f_debug:
                    f_debug.write(driver.page_source)
                print(f"   INFO: HTML da página de erro salvo.")
            except Exception as e_save:
                print(f"   INFO: Falha ao salvar HTML da página de erro: {e_save}")
        return {'url': url, 'title': 'PROCESSING FAILED', 'price': 'N/A'}
    finally:
        if driver: 
            try:
                driver.quit()
            except Exception:
                print(f"   AVISO: Erro ao tentar fechar o driver para {url}. Pode já estar fechado.")

def generate_pdf_report(successful_products, base_url):
    print(f"\n--- GERANDO RELATÓRIO PDF: {PDF_OUTPUT_FILE} ---")
    is_br = "amazon.com.br" in base_url
    currency_symbol = "R$" if is_br else "$"
    report_title = "Relatório dos Mais Vendidos da Amazon (BR)" if is_br else "Amazon Best-Sellers Report"
    date_format = '%d/%m/%Y às %H:%M' if is_br else '%Y-%m-%d at %H:%M'
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        available_width = pdf.w - pdf.r_margin - pdf.l_margin

        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, report_title.encode('latin-1', 'replace').decode('latin-1'), align='C', ln=1) 
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime(date_format)}".encode('latin-1', 'replace').decode('latin-1'), align='C', ln=1) 
        pdf.ln(10) 
        
        for i, product in enumerate(successful_products):
            pdf.set_font('Helvetica', 'B', 10) # Título do produto em negrito
            product_title_text = f"{i+1}. {product['title']}"
            pdf.multi_cell(available_width, 5, product_title_text.encode('latin-1', 'replace').decode('latin-1'))
            
            pdf.set_font('Helvetica', '', 10) # Restante do texto normal
            price_display = product['price']
            if product['price'] not in ["Unavailable", "N/A"] and not product['price'].startswith("Error"):
                try:
                    price_float = float(product['price'])
                    price_display = f"{price_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except (ValueError, TypeError): pass 
            
            price_text = f"   Preco: {currency_symbol}{price_display}"
            pdf.multi_cell(available_width, 5, price_text.encode('latin-1', 'replace').decode('latin-1'))

            # Adicionando o link do produto
            product_url = product['url']
            link_text = f"   Link: {product_url}"
            # Para links, é bom usar uma cor diferente e sublinhado, se a biblioteca suportar facilmente
            # Aqui, vamos apenas adicionar como texto. Para torná-lo clicável, seria mais complexo com FPDF.
            pdf.multi_cell(available_width, 5, link_text.encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(5) # Espaço extra entre os produtos
            
        pdf.output(PDF_OUTPUT_FILE)
        print(f"--- Relatório PDF '{PDF_OUTPUT_FILE}' gerado com sucesso! ---")
    except Exception as e:
        print(f"ERRO AO GERAR PDF: {e}")

if __name__ == '__main__':
    if not os.path.exists(GECKODRIVER_PATH):
        print(f"--- ERRO CRÍTICO: '{GECKODRIVER_PATH}' não encontrado. Coloque-o na pasta do script. ---")
    else:
        links_to_process_raw = encontrar_links_bestsellers_automatico() 
        if links_to_process_raw:
            domain = "https://www.amazon.com.br" if "amazon.com.br" in AMAZON_BEST_SELLERS_URL else "https://www.amazon.com"
            links_info = [{'url': link, 'base_domain': domain} for link in links_to_process_raw]

            mode_message = f"Paralelo ({MAX_WORKERS_STAGE_2} processos)" if MAX_WORKERS_STAGE_2 > 1 else "Sequencial (Modo Estável)"
            print(f"\n--- ETAPA 2 (EXTRAÇÃO DE DADOS): Iniciando extração. MODO = {mode_message} ---")
            
            all_results = []
            if MAX_WORKERS_STAGE_2 > 1: 
                with ThreadPoolExecutor(max_workers=MAX_WORKERS_STAGE_2) as executor:
                    print(f"AVISO: Iniciando {MAX_WORKERS_STAGE_2} processos paralelos. Monitorar por instabilidade e alto uso de recursos.")
                    results_iterator = executor.map(process_one_product, links_info)
                    all_results = list(results_iterator) 
            else: 
                for link_info in links_info:
                    all_results.append(process_one_product(link_info))
                    # Pausa reduzida para tentar acelerar no modo sequencial
                    time.sleep(random.uniform(0.5, 1.0)) 

            successful_results = [res for res in all_results if res and isinstance(res, dict) and "PROCESSING FAILED" not in res.get('title','').upper() and "TITLE NOT FOUND" not in res.get('title','').upper()]
            
            total_attempted = len(all_results)
            num_successful = len(successful_results)
            num_failed = total_attempted - num_successful

            print(f"\n--- Extração finalizada. {num_successful} de {total_attempted} produtos extraídos com dados válidos. ({num_failed} falhas) ---")
            
            if all_results: 
                dict_results = []
                for res in all_results:
                    if isinstance(res, dict):
                        dict_results.append(res)
                    else: 
                        dict_results.append({'url': 'ERRO DESCONHECIDO', 'title': f'Falha Grave no Worker - Retorno: {type(res)}', 'price': 'N/A'})

                df_log = pd.DataFrame(dict_results)
                if 'title' in df_log.columns: 
                    df_log['Status'] = df_log['title'].apply(lambda x: 'Falha' if isinstance(x, str) and ("PROCESSING FAILED" in x.upper() or "TITLE NOT FOUND" in x.upper()) else 'Sucesso')
                else: 
                    df_log['Status'] = 'Falha (sem título)'
                df_log.to_csv(CSV_OUTPUT_FILE, index=False, encoding='utf-8-sig')
                print(f"--- Log CSV '{CSV_OUTPUT_FILE}' salvo. ({len(df_log)} registros) ---")
            
            if successful_results:
                generate_pdf_report(successful_results, AMAZON_BEST_SELLERS_URL)
            else:
                print("--- Nenhum produto com dados válidos para o relatório PDF. ---")
                
    print("\n--- MONITORAMENTO DE PREÇOS FINALIZADO ---")