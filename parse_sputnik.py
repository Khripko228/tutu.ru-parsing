#!/usr/bin/env python3
"""
Парсер расписания электричек
Использование: python3 parse_sputnik.py [фильтр]
Фильтры: all - все рейсы, weekdays - будни, daily - ежедневно
"""

from bs4 import BeautifulSoup
import sys
import os
import re


def parse_schedule(html_file, day_filter='all'):
    """
    Парсер расписания электричек
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return []

    soup = BeautifulSoup(content, 'html.parser')
    trains = []

    # Ищем все элементы с расписанием
    schedule_items = soup.find_all('div', class_='train-item')
    
    for item in schedule_items:
        try:
            # Извлекаем время
            time_elem = item.find('span', class_='time')
            if not time_elem:
                continue
            time = time_elem.get_text(strip=True)
            
            # Извлекаем маршрут
            route_elem = item.find('span', class_='route')
            route = route_elem.get_text(strip=True) if route_elem else "Москва Ярославская"
            
            # Извлекаем дни
            days_elem = item.find('span', class_='days')
            days_text = days_elem.get_text(strip=True).lower() if days_elem else ""
            
            # Определяем тип дней
            is_weekdays = 'будни' in days_text
            is_daily = 'ежедневно' in days_text
            
            # Определяем тип дней для вывода
            if is_daily:
                days_type = 'ежедневно'
            elif is_weekdays:
                days_type = 'будни'
            else:
                days_type = 'ежедневно'
            
            # Применяем фильтр
            if (day_filter == 'all' or 
                (day_filter == 'weekdays' and is_weekdays) or 
                (day_filter == 'daily' and is_daily)):
                
                train_info = {
                    'time': time,
                    'route': route,
                    'days': days_type
                }
                trains.append(train_info)
                    
        except Exception as e:
            continue

    # Сортируем по времени
    trains.sort(key=lambda x: (
        int(x['time'].split(':')[0]),  # часы
        int(x['time'].split(':')[1])   # минуты
    ))
    return trains


def main():
    """Главная функция программы"""
    if not os.path.exists('schedule.html'):
        print("Создаем тестовый файл с расписанием...")
        
        # Создаем качественный тестовый HTML файл
        test_html = """<!DOCTYPE html>
<html>
<head>
    <title>Расписание электричек Москва Ярославская</title>
    <style>
        .schedule { font-family: Arial, sans-serif; margin: 20px; }
        .train-item { 
            border: 1px solid #ddd; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px;
            background: #f9f9f9;
        }
        .time { 
            font-weight: bold; 
            color: #2c3e50; 
            font-size: 18px;
            margin-right: 20px;
        }
        .route { 
            color: #34495e;
            margin-right: 20px;
        }
        .days { 
            color: #7f8c8d; 
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="schedule">
        <h1>Расписание электричек</h1>
        <h2>Станция: Москва Ярославская</h2>
        
        <div class="train-item">
            <span class="time">05:45</span>
            <span class="route">Москва Ярославская → Щёлково</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">06:15</span>
            <span class="route">Москва Ярославская → Александров</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">06:45</span>
            <span class="route">Москва Ярославская → Пушкино</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">07:20</span>
            <span class="route">Москва Ярославская → Мытищи</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">07:45</span>
            <span class="route">Москва Ярославская → Красноармейск</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">08:15</span>
            <span class="route">Москва Ярославская → Сергиев Посад</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">08:45</span>
            <span class="route">Москва Ярославская → Болшево</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">09:20</span>
            <span class="route">Москва Ярославская → Фрязино</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">17:30</span>
            <span class="route">Москва Ярославская → Щёлково</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">18:15</span>
            <span class="route">Москва Ярославская → Александров</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">19:00</span>
            <span class="route">Москва Ярославская → Пушкино</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">19:45</span>
            <span class="route">Москва Ярославская → Мытищи</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">20:30</span>
            <span class="route">Москва Ярославская → Красноармейск</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">21:15</span>
            <span class="route">Москва Ярославская → Сергиев Посад</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">22:00</span>
            <span class="route">Москва Ярославская → Болшево</span>
            <span class="days">будни</span>
        </div>
        <div class="train-item">
            <span class="time">22:45</span>
            <span class="route">Москва Ярославская → Фрязино</span>
            <span class="days">ежедневно</span>
        </div>
        <div class="train-item">
            <span class="time">23:30</span>
            <span class="route">Москва Ярославская → Щёлково</span>
            <span class="days">ежедневно</span>
        </div>
    </div>
</body>
</html>"""
        
        with open('schedule.html', 'w', encoding='utf-8') as f:
            f.write(test_html)
        print("Качественный тестовый файл schedule.html создан!")

    # Определяем фильтр
    day_filter = 'all'
    if len(sys.argv) > 1:
        filter_arg = sys.argv[1].lower()
        if filter_arg in ['weekdays', 'будни']:
            day_filter = 'weekdays'
        elif filter_arg in ['daily', 'ежедневно']:
            day_filter = 'daily'

    print(f"🗓 Парсим расписание электричек...")
    print(f"🔍 Фильтр: {day_filter}")
    print("=" * 60)

    trains = parse_schedule('schedule.html', day_filter)

    if not trains:
        print("❌ Рейсы не найдены.")
        return

    # Выводим результаты
    for i, train in enumerate(trains, 1):
        print(f"{i:2d}. 🕒 {train['time']} | 🚆 {train['route']} | 📅 [{train['days']}]")

    print("=" * 60)
    print(f"✅ Всего рейсов: {len(trains)}")


if __name__ == "__main__":
    main()