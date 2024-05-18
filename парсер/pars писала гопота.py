import os
import json

# Получаем путь к текущему каталогу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Открываем файл pci.ids для чтения
with open(os.path.join(current_dir, 'pci.ids'), 'r') as file:
    # Инициализируем пустой словарь для хранения данных
    pci_data = {}
    current_vendor_id = None
    current_vendor_name = None

    # Читаем файл построчно
    for line in file:
        # Удаляем символы новой строки в конце строки
        line = line.strip()

        # Пропускаем пустые строки и строки комментариев
        if not line or line.startswith('#'):
            continue

        # Если строка начинается с символа табуляции, это описание устройства,
        # иначе это описание вендора
        if line.startswith('\t'):
            # Разбиваем строку по символу табуляции
            parts = line.split('\t')
            # Добавляем описание устройства в словарь pci_data
            pci_data[current_vendor_id]['devices'].append({
                'id': parts[0].strip(),
                'name': parts[1].strip()
            })
        else:
            # Разбиваем строку по символу пробела
            parts = line.split(' ', 1)
            # Получаем идентификатор вендора и его имя
            current_vendor_id = parts[0].strip()
            current_vendor_name = parts[1].strip()
            # Добавляем вендора в словарь pci_data
            pci_data[current_vendor_id] = {
                'name': current_vendor_name,
                'devices': []
            }

# Записываем данные в JSON-файл
with open(os.path.join(current_dir, 'pci_data.json'), 'w') as json_file:
    json.dump(pci_data, json_file, indent=4)
