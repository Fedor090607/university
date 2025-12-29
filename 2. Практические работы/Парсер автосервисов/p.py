import re
import csv
import ssl
import urllib.request

url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"
# Функция urlopen() открывает указанный URL и возвращает объект ответа для чтения данных
response = urllib.request.urlopen(url)
# Метод read() читает данные как байты, decode() преобразует их в строку UTF-8
html_content = response.read().decode('utf-8')

# Сохраняем HTML в файл для отладки (необязательный шаг)
with open('t.txt', mode='w', encoding='utf-8') as file:
    file.write(html_content)

# r'' - сырая строка, в которой экранируются обратные слеши
# \s* - пробельные символы (0 или более)
# .*? - любой символ в нежадном режиме (0 или более)
# ([^<]+?) - группа захвата: все символы кроме '<' в нежадном режиме (1 или более)
re_algorithm = r'class="org-widget-header__title-link">\s*([^<]+?)\s*</a>.*?' \
               r'org-widget-header__meta--location">\s*([^<]+?)\s*</span>.*?' \
               r'<dt class="spec__index"><span class="spec__index-inner">Телефон</span></dt>.*?' \
               r'<dd class="spec__value">\s*([^<]+?)\s*</dd>.*?' \
               r'<dt class="spec__index"><span class="spec__index-inner">Часы работы</span></dt>.*?' \
               r'<dd class="spec__value">\s*([^<]+?)\s*</dd>'

# Функция findall возвращает список всех непересекающихся совпадений в виде кортежей
# re.DOTALL - модификатор, при котором символ '.' соответствует также символу новой строки
matches = re.findall(re_algorithm, html_content, re.DOTALL)

# Очищаем данные: удаляем лишние пробелы в начале и конце каждого значения
cleaned_matches = [(name.strip(), address.strip(), phone.strip(), hours.strip())
    for name, address, phone, hours in matches]

# Сохраняем данные в CSV файл
with open('c.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    
    # Записываем заголовки столбцов
    writer.writerow(['Наименование', 'Адрес', 'Телефон', 'Часы работы'])
    # Записываем все строки данных
    writer.writerows(cleaned_matches)
