import threading
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from colorama import init, Fore, Style

init(autoreset=True)

logging.getLogger('selenium').setLevel(logging.WARNING)
chrome_logger = logging.getLogger('chromedriver')
chrome_logger.setLevel(logging.ERROR)

active_drivers = []
cleanup_done = False

def cleanup():
    global cleanup_done
    if not cleanup_done:
        print(f"{Fore.YELLOW}Cleanup:{Style.RESET_ALL} Closing all browser instances...")
        for driver in active_drivers:
            try:
                driver.quit()
            except:
                pass
        print(f"{Fore.GREEN}Cleanup:{Style.RESET_ALL} All browser instances closed.")
        cleanup_done = True

def load_proxies(filename='proxies.txt'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def setup_chrome(proxy=None):
    options = Options()
    options.add_experimental_option("detach", True)
    if proxy:
        options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

def launch_browser(proxy=None, username="TerBot.bar"):
    options = setup_chrome(proxy)
    driver = webdriver.Chrome(options=options)
    active_drivers.append(driver)
    
    driver.set_window_size(1336, 768)
    driver.get("https://territorial.io")

    input = driver.find_element(By.ID, "inputUsername")
    input.clear()
    input.send_keys(username)
    print(f"{Fore.GREEN}Info:{Style.RESET_ALL} Set username '{username}' in {threading.current_thread().name}")

    driver.find_element(By.CSS_SELECTOR, "button[style*='background-color: rgba(0, 70, 0, 0.85);']").click()
    print(f"{Fore.GREEN}Info:{Style.RESET_ALL} Clicked Multiplayer in {threading.current_thread().name}")
    time.sleep(7.5)

    return driver

def select_game(driver, game_id):
    game_coords = {
        1: (450, 200), 2: (600, 200), 3: (800, 200),
        4: (450, 400), 5: (600, 400), 6: (800, 400), 7: (700,300)
    }

    if game_id in game_coords:
        x, y = game_coords[game_id]
        ActionChains(driver).move_by_offset(x, y).click().perform()
        print(f"{Fore.GREEN}Info:{Style.RESET_ALL} Joined game in {threading.current_thread().name}")
    else:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Invalid game ID in {threading.current_thread().name}")

def main():
    #clan_tag = input("Enter clan tag for bots, without brackets (optional, press Enter to skip): ").strip()
    username = input("Enter bot name: ").strip()
    
    #username = f"[{clan_tag}] TerriBot Github" if clan_tag else "TerriBot Github"
    
    while True:
        try:
            bot_count = int(input("Number of bot instances to run: "))
            if bot_count > 0:
                break
            print("Enter a positive number.")
        except ValueError:
            print("Invalid input. Enter a number.")
    
    use_proxies = input("Use proxies? (y/N): ").strip().lower() == 'y'
    
    drivers = []
    threads = []

    if use_proxies:
        proxies = load_proxies()
        if bot_count > len(proxies):
            print(f"{Fore.RED}Error:{Style.RESET_ALL} Not enough proxies for {bot_count} bots.")
            return
        for i in range(bot_count):
            t = threading.Thread(target=lambda: drivers.append(launch_browser(proxies[i], username)), name=f"Bot-{i+1}")
            t.start()
            threads.append(t)
            print(f"{Fore.CYAN}Info:{Style.RESET_ALL} Bot started with proxy {proxies[i]} (Thread: {t.name})")
            time.sleep(1)
    else:
        for i in range(bot_count):
            t = threading.Thread(target=lambda: drivers.append(launch_browser(username=username)), name=f"Bot-{i+1}")
            t.start()
            threads.append(t)
            print(f"{Fore.CYAN}Info:{Style.RESET_ALL} Bot started (Thread: {t.name})")
            time.sleep(1)

    for t in threads:
        t.join()

    game_id = int(input(f"{Fore.CYAN}Input:{Style.RESET_ALL} Which game ID to join (7 = Contest): "))

    for driver in drivers:
        select_game(driver, game_id)
        
    if input(f"{Fore.CYAN}Input:{Style.RESET_ALL} Type 'quit' to close browsers: ").strip().lower() == 'quit':
        print(f"{Fore.GREEN}Info:{Style.RESET_ALL} Closing all browsers.")
        cleanup()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} Unexpected error: {e}")
        print(f"{Fore.YELLOW}Cleanup:{Style.RESET_ALL} Attempting to close all browsers...")
    finally:
        cleanup()
