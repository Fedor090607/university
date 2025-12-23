import re
import csv
import ssl
import urllib.request

#страницу берет и сохр в файл
url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"
response = urllib.request.urlopen(url)
html_content = response.read().decode()
with open('html.txt', mode='w', encoding='utf8') as file:
    file.write(html_content)

#[^<] любой символу кроме <
#\s* для удал ненужных пробелов
#+? квантификатор 1 или более кроме <
#.*? любой символ кроме переноса строки 
re_algorithm = r'class="org-widget-header__title-link">\s*([^<]+?)\s*</a>.*?' \
               r'org-widget-header__meta--location">\s*([^<]+?)\s*</span>.*?' \
               r'<dt class="spec__index"><span class="spec__index-inner">Телефон</span></dt>.*?' \
               r'<dd class="spec__value">\s*([^<]+?)\s*</dd>.*?' \
               r'<dt class="spec__index"><span class="spec__index-inner">Часы работы</span></dt>.*?' \
               r'<dd class="spec__value">\s*([^<]+?)\s*</dd>'

# поиск совпадений по регуляркам
matches = re.findall(re_algorithm, html_content, re.DOTALL)

cleaned_matches = [(name.strip(), address.strip(), phone.strip(), hours.strip()) for name, address, phone, hours in matches]

# запись результатов в csv с запятой
with open('output.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') 

    writer.writerow(['Наименование', 'Адрес', 'Телефон', 'Часы работы'])
    #строки данных
    writer.writerows(cleaned_matches)
