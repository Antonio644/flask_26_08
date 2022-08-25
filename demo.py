import json

quotes = [(1, 'Rick Cook', 'Программирование сегодня — это гонка разработчиков программ...'),
          (2, 'Waldi Ravens', 'Программирование на С похоже на быстрые танцы на только...')]

keys = ['id', 'author', 'text']

quotes_dict = []

for i in quotes:
    quotes_dict.append(set(i))
print(quotes_dict)