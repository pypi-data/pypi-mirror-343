import socket
import requests

def get_local_ip_address():
    """
    Получает локальный IP-адрес устройства.
    
    Returns:
        str: Локальный IP-адрес или None в случае ошибки.
    """
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error as e:
        raise RuntimeError(f"Ошибка при получении локального IP: {e}")

def get_external_ip_address():
    """
    Получает внешний IP-адрес через сервис https://httpbin.org/ip.
    
    Returns:
        str: Внешний IP-адрес или None в случае ошибки.
    """
    try:
        response = requests.get('https://httpbin.org/ip', timeout=5)
        response.raise_for_status()
        return response.json()['origin']
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при получении внешнего IP: {e}")

def get_country_by_ip(ip_address):
    """
    Определяет страну по IP-адресу через сервис https://ipinfo.io.
    
    Args:
        ip_address (str): IP-адрес для проверки.
    
    Returns:
        str: Код страны (например, 'RU') или 'Неизвестно'.
    """
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
        response.raise_for_status()
        return response.json().get('country', 'Неизвестно')
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при определении страны: {e}")
