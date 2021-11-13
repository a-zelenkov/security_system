import json
import utils


DATABASE_FILE = 'db.json'

try:
    with open(DATABASE_FILE, 'r', encoding='utf-8') as read_file:
        persons = json.load(read_file)
except:
    persons = []

LAST_PERSON_ID = 0

for person in persons:
    if person['id'] >= LAST_PERSON_ID:
        LAST_PERSON_ID = person['id'] + 1

print('Добавление лица в базу данных')
print('1 - с существующего изображения')
print('2 - сделать снимок с веб-камеры')
method = 0
while not method in range(1,3):
    method = int(input('Введите метод: '))

if method == 1:
    file = input('Введите абсолютный путь к изображению: ')
    person_face = utils.getFaceFromImg(file)
if method == 2:
    person_face = utils.getFaceFromWebCam()


if not person_face is None:
    print('Добавление информации')

    new_person = {
        'id': LAST_PERSON_ID,
        'name_russian': input('Введите имя (на русском): '),
        'name': input('Введите имя (на английском): '),
        'face': person_face
    }

persons.append(new_person)

try:
    with open(DATABASE_FILE, 'w', encoding='utf-8') as write_file:
        json.dump(persons, write_file, ensure_ascii=False)
        print('База данных успешно обновлена')
except:
    print('Возникла ошибка при попытке обновить базу данных')