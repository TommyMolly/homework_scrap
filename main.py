import requests
import json
import re
from time import sleep


def get_vacancies(page):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'python',
        'area': [1, 2],  # MSK и SPB
        'page': page,
        'per_page': 100
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе данных: {response.status_code}")
        return None


def filter_vacancies(vacancies):
    result = []
    for item in vacancies['items']:
        description = item.get('snippet', {}).get('responsibility', '')

        if isinstance(description, str) and re.search(r'\b(Django|Flask)\b', description, re.IGNORECASE):
            result.append({
                'title': item['name'],
                'link': item['alternate_url'],
                'company': item['employer']['name'],
                'salary': item['salary'],
                'city': item['area']['name']
            })

    return result


def main():
    all_vacancies = []

    for page in range(5):
        vacancies = get_vacancies(page)
        if vacancies:
            filtered_vacancies = filter_vacancies(vacancies)
            all_vacancies.extend(filtered_vacancies)
        sleep(1)

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=4)

    print(f"Найдено и записано {len(all_vacancies)} вакансий")


if __name__ == '__main__':
    main()
