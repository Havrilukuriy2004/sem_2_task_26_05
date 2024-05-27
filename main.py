import requests
import re
from datetime import datetime

def get_weather_forecast(city_name):
    url = f'https://ua.sinoptik.ua/погода-{city_name}'
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    page_content = response.text
    current_date_pattern = re.compile(
        r'data-link="//ua\.sinoptik\.ua/погода-[^/]+/(\d{4}-\d{2}-\d{2})"',
        re.DOTALL
    )
    current_date_match = current_date_pattern.search(page_content)
    if current_date_match:
        current_date = current_date_match.group(1)
    else:
        current_date = datetime.now().strftime('%Y-%m-%d')

    print(f"Поточна дата: {current_date}")
    date_pattern = re.compile(
        r'(?:href|data-link)="//ua\.sinoptik\.ua/погода-[^/]+/(\d{4}-\d{2}-\d{2})">',
        re.DOTALL
    )
    dates = date_pattern.findall(page_content)

    forecast_pattern = re.compile(
        r'<div class="temperature">.*?<div class="min">.*?<span>([\+\-]?\d+)&deg;</span>.*?'
        r'<div class="max">.*?<span>([\+\-]?\d+)&deg;</span>',
        re.DOTALL
    )
    forecast_matches = forecast_pattern.findall(page_content)

    if len(dates) < 7 or len(forecast_matches) < 7:
        raise ValueError('Недостатньо даних для прогнозу на 7 днів.')

    weather_forecast = []
    for i in range(7):
        date = dates[i]
        min_temp, max_temp = forecast_matches[i]
        weather_forecast.append((date, min_temp, max_temp))

    return weather_forecast

def display_forecast(weather_forecast):
    for date, min_temp, max_temp in weather_forecast:
        print(f"{date}: Мінімальна температура: {min_temp}°C, Максимальна температура: {max_temp}°C")

if __name__ == '__main__':
    city_name = input('Введіть назву міста українською: ').strip()
    try:
        weather_forecast = get_weather_forecast(city_name)
        display_forecast(weather_forecast)
    except Exception as e:
        print(f"Error: {e}")
