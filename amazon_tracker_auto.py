import pandas as pd
from datetime import datetime
import os
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF, XPos, YPos
import glob 
import re 

# Importações do Selenium para Firefox
from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÃO ---
CSV_OUTPUT_FILE = 'historico_precos_BR_auto.csv' 
PDF_OUTPUT_FILE = 'Relatorio_Mais_Vendidos_BR_auto.pdf'

# --- MODO DE EXECUÇÃO ---
# O modo paralelo (valor > 1) se mostrou instável e causou erros.
# Mantendo em 1 para garantir a extração de todos os produtos sem falhas.
MAX_WORKERS_STAGE_2 = 1

# URL da página de Mais Vendidos da Amazon BRASIL
AMAZON_BEST_SELLERS_URL = "https://www.amazon.com.br/gp/bestsellers/electronics/"
# Caminho para o geckodriver.exe. Coloque o executável na mesma pasta do script.
GECKODRIVER_PATH = "geckodriver.exe" 

USER_AGENTS_FOR_SELENIUM = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

def get_profile_path(profile_name='default-release'):
    """Tenta encontrar o perfil padrão do Firefox para usar cookies e sessões existentes."""
    try:
        base_path = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
        if not os.path.exists(base_path): 
            print("AVISO: Diretório de perfis do Firefox não encontrado. O script continuará sem um perfil pré-carregado.")
            return None
        profile_directories = glob.glob(os.path.join(base_path, f'*.{profile_name}'))
        if not profile_directories:
            print(f"AVISO: Nenhum perfil do Firefox terminando em '{profile_name}' foi encontrado.")
            return None
        profile_directory = profile_directories[0]
        print(f"Usando o perfil do Firefox encontrado em: {profile_directory}")
        return profile_directory
    except Exception as e:
        print(f"Não foi possível encontrar o perfil do Firefox: {e}")
        return None

FIREFOX_PROFILE_PATH = get_profile_path()

def encontrar_links_bestsellers_automatico():
    """ETAPA 1: Usa Selenium/Firefox para buscar os links dos produtos."""
    print(f"--- ETAPA 1 (SELENIUM/FIREFOX): Acessando {AMAZON_BEST_SELLERS_URL} ---")
    driver = None
    try:
        options = Options()
        if FIREFOX_PROFILE_PATH:
            options.add_argument("-profile")
            options.add_argument(FIREFOX_PROFILE_PATH)
        options.set_preference("general.useragent.override", random.choice(USER_AGENTS_FOR_SELENIUM))
        
        service = Service(executable_path=GECKODRIVER_PATH)
        driver = webdriver.Firefox(service=service, options=options)
        
        print(f" -> Navegando para a página dos Mais Vendidos...")
        driver.get(AMAZON_BEST_SELLERS_URL)
        
        print("\n>>> ATENÇÃO: Uma janela do Firefox foi aberta. <<<")
        print(">>> Se a página pedir um CAPTCHA, resolva-o MANUALMENTE para continuar.")
        print(">>> O script aguardará até que a lista de produtos seja encontrada (máx 2 minutos)... <<<\n")
        
        wait = WebDriverWait(driver, 120)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id^='p13n-asin-index-']")))
        print(" -> Lista de produtos encontrada. Extraindo links...")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_items = soup.select("div[id^='p13n-asin-index-']")
        
        if not product_items:
            print("ERRO: Nenhum item de produto encontrado.")
            return []

        product_links = []
        parsed_url_base = "/".join(AMAZON_BEST_SELLERS_URL.split("/")[:3])
        for item in product_items:
            link_tag = item.select_one('a.a-link-normal[href*="/dp/"]')
            if link_tag and 'href' in link_tag.attrs:
                href = link_tag['href'].split('/ref=')[0]
                url_complete = parsed_url_base + href if not href.startswith('http') else href
                if url_complete not in product_links:
                    product_links.append(url_complete)
                if len(product_links) >= 50:
                    break
        
        print(f"--- {len(product_links)} links de produtos encontrados com sucesso! ---")
        return product_links
    except Exception as e:
        print(f"Falha CRÍTICA na Etapa 1 (Selenium): {type(e).__name__} - {e}")
        return []
    finally:
        if driver:
            driver.quit()
            print(" -> Navegador da Etapa 1 fechado.")

def clean_price(price_text_input, domain_base):
    """Limpa e valida o texto do preço."""
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
    """ETAPA 2: Extrai dados de uma página de produto individual."""
    url = url_info['url']
    base_domain = url_info['base_domain']
    driver = None
    display_url = url[:70] + "..." if len(url) > 70 else url
    print(f" -> Processando: {display_url}") 

    try:
        options = Options()
        if FIREFOX_PROFILE_PATH:
            options.add_argument("-profile")
            options.add_argument(FIREFOX_PROFILE_PATH)
        options.add_argument("-headless") 
        options.set_preference("general.useragent.override", random.choice(USER_AGENTS_FOR_SELENIUM))
        
        service = Service(executable_path=GECKODRIVER_PATH)
        driver = webdriver.Firefox(service=service, options=options)
        
        driver.get(url)
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "productTitle")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title_element = soup.find('span', id='productTitle')
        title = title_element.get_text(strip=True) if title_element else 'Title not found'
        price = 'Unavailable'
        currency_symbol = "R$" if "amazon.com.br" in base_domain else "$"

        if title != 'Title not found':
            price_element = soup.select_one('span.a-price.a-text-price span.a-offscreen, #corePrice_feature_div span.a-offscreen')
            if price_element:
                cleaned_price = clean_price(price_element.get_text(strip=True), base_domain)
                if "Error" not in cleaned_price:
                    price = cleaned_price

        if title != 'Title not found':
            print(f"   [OK] Extraído: {title[:40]}... | Preço: {currency_symbol}{price}")
        else:
            print(f"   [FALHA] Título não encontrado para: {url}")
            
        return {'url': url, 'title': title, 'price': price}
    except Exception as e:
        print(f"   [FALHA] Erro ao processar {url}: {type(e).__name__}")
        return {'url': url, 'title': 'PROCESSING FAILED', 'price': 'N/A'}
    finally:
        if driver: driver.quit()

def generate_pdf_report(successful_products, base_url):
    """Gera o relatório em PDF com correção final para o bug de layout."""
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
        title_encoded = report_title.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 10, title_encoded, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font('Helvetica', '', 11)
        date_text = f"Gerado em: {datetime.now().strftime(date_format)}"
        date_encoded = date_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 10, date_encoded, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)

        # Usar uma fonte consistente para todos os produtos
        pdf.set_font('Helvetica', '', 10)
        
        for i, product in enumerate(successful_products):
            # Prepara o texto do preço
            price_display = product['price']
            if product['price'] not in ["Unavailable", "N/A"] and not product['price'].startswith("Error"):
                try:
                    price_float = float(product['price'])
                    price_display = f"{price_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except (ValueError, TypeError): pass 
            
            # Combina título e preço em um único bloco de texto
            product_title = f"{i+1}. {product['title']}"
            price_text = f"   Preco: {currency_symbol}{price_display}"
            full_text_block = f"{product_title}\n{price_text}"
            
            # Codifica o bloco inteiro e usa multi_cell uma única vez por produto
            text_encoded = full_text_block.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(available_width, 5, text_encoded)
            pdf.ln(5) # Adiciona um espaço extra entre os produtos

        pdf.output(PDF_OUTPUT_FILE)
        print(f"--- Relatório PDF '{PDF_OUTPUT_FILE}' gerado com sucesso! ---")
    except Exception as e:
        print(f"ERRO AO GERAR PDF: {e}")

if __name__ == '__main__':
    links_to_process_raw = encontrar_links_bestsellers_automatico() 
    
    if links_to_process_raw:
        domain = "https://www.amazon.com.br" if "amazon.com.br" in AMAZON_BEST_SELLERS_URL else "https://www.amazon.com"
        links_info = [{'url': link, 'base_domain': domain} for link in links_to_process_raw]

        mode_message = "Sequencial (Modo Estável)"
        print(f"\n--- ETAPA 2 (EXTRAÇÃO DE DADOS): Iniciando extração. MODO = {mode_message} ---")
        
        all_results = []
        # Loop simples para execução sequencial
        for link_info in links_info:
            all_results.append(process_one_product(link_info))
            time.sleep(random.uniform(1, 3)) # Pequena pausa para ser gentil com o servidor da Amazon

        successful_results = [res for res in all_results if res and "FAILED" not in res['title']]
        
        print(f"\n--- Extração finalizada. {len(successful_results)} de {len(all_results)} produtos foram extraídos. ---")
        
        if all_results: 
            df_log = pd.DataFrame(all_results)
            df_log.to_csv(CSV_OUTPUT_FILE, index=False, encoding='utf-8-sig')
            print(f"--- Log completo em CSV '{CSV_OUTPUT_FILE}' salvo com sucesso! ---")
        
        if successful_results:
            generate_pdf_report(successful_results, AMAZON_BEST_SELLERS_URL)
        else:
            print("--- Nenhum produto com dados válidos foi extraído para o relatório em PDF. ---")
            
    print("\n--- MONITORAMENTO DE PREÇOS FINALIZADO ---")