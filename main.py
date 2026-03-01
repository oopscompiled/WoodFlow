import openpyxl
from datetime import datetime, timedelta
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import json
import os

# Получение текущей даты
today = datetime.now()
year = today.year
month = today.month

# Получение названия месяца на русском
months_ru = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
}
month_name = months_ru[month]

# Пути к папкам
desktop_reports = '/Users/mihailpopov/Desktop/Отчёты'
template_file = 'шаблон.xlsx'
output_file = os.path.join(desktop_reports, f'{month_name}.xlsx')
shift_log_file = os.path.join(desktop_reports, 'shift_log.json')

# Создание папки если её нет
if not os.path.exists(desktop_reports):
    os.makedirs(desktop_reports)

# Загрузка последнего состояния смен
if os.path.exists(shift_log_file):
    with open(shift_log_file, 'r') as f:
        shift_data = json.load(f)
    shift_counter = shift_data['shift_counter']
    last_month = shift_data['month']
    
    # Если месяц изменился, продолжаем цикл
    if last_month != month:
        shift_counter = (shift_counter + 1) % 4
else:
    shift_counter = 0

# Загрузка шаблона
wb = openpyxl.load_workbook(template_file)
template_ws = wb.active

# Получение количества дней в месяце
if month == 12:
    last_day = (datetime(year + 1, 1, 1) - timedelta(days=1)).day
else:
    last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day

# Генерация листов для каждой смены (2/2)
current_date = datetime(year, month, 1)
sheet_count = 0
first_sheet = True

while current_date.month == month:
    if shift_counter < 2:  # Рабочие дни
        date_str = current_date.strftime("%d.%m.%Y")
        
        # Переименование первого листа или копирование шаблона
        if first_sheet:
            new_ws = template_ws
            new_ws.title = date_str
            first_sheet = False
        else:
            new_ws = wb.copy_worksheet(template_ws)
            new_ws.title = date_str
        
        # Редактирование шаблона под дату
        new_ws['G3'] = f"Отчёт: {date_str}"
        
        sheet_count += 1
        current_date += timedelta(days=1)
    else:  # Выходные дни
        current_date += timedelta(days=1)
    
    shift_counter = (shift_counter + 1) % 4  # Цикл 0,1,2,3

# Сохранение текущего состояния смен
with open(shift_log_file, 'w') as f:
    json.dump({'shift_counter': shift_counter, 'month': month}, f)

# Сохранение файла
wb.save(output_file)
print(f"Файл создан: {output_file}")
print(f"Листов с датами: {sheet_count}")
print(f"Следующая смена начнётся со статуса: {shift_counter}")