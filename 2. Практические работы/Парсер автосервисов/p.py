import re
import csv
import ssl
import urllib.request

url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"
response = urllib.request.urlopen(url) #функция открывает указанный URL и возвращает объект ответа, позволяющий читать данные
html_content = response.read().decode() #читает данные как байты и превращает их в строку.

with open('t.txt', mode='w', encoding='utf8') as file:
    file.write(html_content) #записать строку в файл
    
#r'' напиши нейронка
# \s* пробельные символы от 0 и более
# .*? любой символ в ленивом режиме от 0 и более
# ([^<]+?) группа захвата все кроме < в ленивом режиме от 1 и более раз
re_algorithm = r'class="org-widget-header__title-link">\s*([^<]+?)\s*</a>.*?' \
               r'org-widget-header__meta--location">\s*([^<]+?)\s*</span>.*?' \
               r'<dt class="spec__index"><span class="spec__index-inner">Телефон</span></dt>.*?' \
               r'<dd class="spec__value">\s*([^<]+?)\s*</dd>.*?' \
               r'<dt class="spec__index"><span class="spec__index-inner">Часы работы</span></dt>.*?' \
               r'<dd class="spec__value">\s*([^<]+?)\s*</dd>'

#функция re.findall возвращает список всех совпадений в строке.
matches = re.findall(re_algorithm, html_content, re.DOTALL) #Флаг (модификатор) Символ .  соответствует символу новой строки \n
cleaned_matches = [(name.strip(), address.strip(), phone.strip(), hours.strip()) for name, address, phone, hours in matches]

with open('c.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') 

    writer.writerow(['Наименование', 'Адрес', 'Телефон', 'Часы работы']) #для записи одного списка
    writer.writerows(cleaned_matches) #для записи нескольких списков
