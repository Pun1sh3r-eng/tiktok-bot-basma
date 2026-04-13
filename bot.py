import os
import random
import time
import threading
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Renkleri başlat
init(autoreset=True)

class TikTokBot:
    def __init__(self, proxy_file="proxy.txt"):
        self.proxies = self.load_proxies(proxy_file)
        if not self.proxies:
            print(f"{Fore.RED}[HATA] Proxy dosyası bulunamadı veya boş: {proxy_file}")
            print(f"{Fore.YELLOW}Lütfen proxy.txt dosyasını oluşturun ve içine proxy'ler ekleyin.")
            exit()
        print(f"{Fore.GREEN}[BAŞARILI] {len(self.proxies)} adet proxy yüklendi.")

    def load_proxies(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            proxies = [line.strip() for line in f if line.strip() and ':' in line]
        return proxies

    def get_random_proxy(self):
        return random.choice(self.proxies)

    def setup_driver(self):
        proxy = self.get_random_proxy()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--proxy-server={proxy}")
        
        # Termux için chromedriver yolunu belirtin
        chrome_options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
        
        # User-Agent rastgele seçimi
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print(f"{Fore.CYAN}[BİLGİ] Proxy ile başlatıldı: {proxy}")
            return driver
        except Exception as e:
            print(f"{Fore.RED}[HATA] Selenium WebDriver başlatılamadı: {e}")
            print(f"{Fore.YELLOW}[BİLGİ] Lütfen chromium ve chromium-driver'ın doğru kurulduğundan emin olun.")
            return None

    def send_request(self, service_type, target, count, delay):
        driver = self.setup_driver()
        if not driver:
            return False

        try:
            # Burada zefoy.com veya benzeri bir hizmetin API'sini kullanabiliriz.
            # Örnek olarak, sahte bir URL ve elementler kullanıyorum.
            # Gerçek kullanımda bu kısmı hedef sitenin yapısına göre düzenlemeniz gerekir.
            
            # Hedef siteye git (örnek)
            driver.get(f"https://zefoy.com/{service_type}")
            time.sleep(2)

            # Hedefi gir (video URL veya kullanıcı adı)
            target_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "target_input"))
            )
            target_input.clear()
            target_input.send_keys(target)
            
            # Gönder butonuna tıkla
            send_button = driver.find_element(By.ID, "send_button")
            
            for i in range(count):
                send_button.click()
                print(f"{Fore.MAGENTA}[İŞLEM] {service_type} gönderildi: {i+1}/{count}")
                time.sleep(delay)
                
                # Her istekten sonra proxy değiştir
                driver.quit()
                driver = self.setup_driver()
                if not driver:
                    print(f"{Fore.RED}[HATA] Proxy değiştirilemedi, işlem durduruluyor.")
                    break
                driver.get(f"https://example.com/{service_type}")
                time.sleep(2)
                target_input = driver.find_element(By.ID, "target_input")
                target_input.clear()
                target_input.send_keys(target)
                send_button = driver.find_element(By.ID, "send_button")

            return True
        except Exception as e:
            print(f"{Fore.RED}[HATA] İstek gönderilirken hata oluştu: {e}")
            return False
        finally:
            if driver:
                driver.quit()

def show_menu():
    print(f"\n{Style.BRIGHT}{Fore.CYAN}========================================")
    print(f"{Fore.YELLOW}     TikTok Otomasyon Aracı")
    print(f"{Fore.CYAN}========================================{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[1] İzlenme Gönder")
    print(f"{Fore.GREEN}[2] Beğeni Gönder")
    print(f"{Fore.GREEN}[3] Takipçi Gönder")
    print(f"{Fore.RED}[0] Çıkış")
    print(f"{Style.BRIGHT}{Fore.CYAN}========================================{Style.RESET_ALL}")

def main():
    bot = TikTokBot()
    
    while True:
        show_menu()
        choice = input(f"{Fore.BLUE}[SEÇİM] Yapmak istediğiniz işlemi seçin: ")
        
        if choice == "0":
            print(f"{Fore.YELLOW}[BİLGİ] Programdan çıkılıyor...")
            break
            
        if choice not in ["1", "2", "3"]:
            print(f"{Fore.RED}[HATA] Geçersiz seçim, lütfen tekrar deneyin.")
            continue
            
        target = input(f"{Fore.BLUE}[HEDEF] Video URL'sini veya kullanıcı adını girin: ")
        try:
            count = int(input(f"{Fore.BLUE}[ADET] Gönderilecek miktarı girin: "))
            delay = int(input(f"{Fore.BLUE}[GEÇİKME] İstekler arası gecikme (saniye): "))
        except ValueError:
            print(f"{Fore.RED}[HATA] Lütfen sayısal bir değer girin.")
            continue
            
        service_map = {
            "1": "views",
            "2": "likes",
            "3": "followers"
        }
        
        service_type = service_map[choice]
        
        # Çoklu thread ile işlemi başlat
        print(f"{Fore.YELLOW}[BİLGİ] {count} adet {service_type} gönderimi başlatılıyor...")
        thread = threading.Thread(
            target=bot.send_request,
            args=(service_type, target, count, delay)
        )
        thread.start()
        thread.join()  # İşlemin bitmesini bekle
        
        print(f"{Fore.GREEN}[BAŞARILI] İşlem tamamlandı.")

if __name__ == "__main__":
    main()
