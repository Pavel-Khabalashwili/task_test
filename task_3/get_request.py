import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def send_request(url):
    """
    Отправляет GET-запрос к указанному URL и возвращает код статуса ответа.
    """
    try:
        response = requests.get(url)
        return response.status_code 
    except requests.RequestException as e:
        return str(e) 

def main():
    """
    Основная функция для запуска программы.
    """
    url = input("Введите URL-адрес ресурса: ") 
    number_of_requests = 1000 


    with ThreadPoolExecutor(max_workers=100) as executor:
        with tqdm(total=number_of_requests, desc="Отправка запросов") as progress:
        
            futures = [executor.submit(send_request, url) for _ in range(number_of_requests)]
            for future in futures:
                future.result() 
                progress.update(1)  

if __name__ == "__main__":
    main()