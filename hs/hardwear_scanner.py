import wmi
import json
import os
import platform

def get_vendor_name(device_id):
    current_dir = os.path.dirname(__file__) 
    file_path = os.path.join(current_dir, 'pci_data.json')
    with open(file_path, 'r') as file:
        ddr_types = json.load(file)
        return ddr_types.get(str(device_id), "Неизвестно")

def get_ddr_type(memory_type):
    current_dir = os.path.dirname(__file__) 
    file_path = os.path.join(current_dir, 'memory_types.json')
    with open(file_path, 'r') as file:
        ddr_types = json.load(file)
        return ddr_types.get(str(memory_type), "Неизвестно")

def save_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(item + '\n')

def run_script(remote_computer=None):
    if not remote_computer:
        c = wmi.WMI()
    else:
        c = wmi.WMI(computer=remote_computer)

    data_to_save = []

    current_computer = platform.node()
    data_to_save.append(f"Имя компьютера: {current_computer}\n")
    
    for motherboard in c.Win32_BaseBoard():
        data_to_save.append("Материнская плата:")
        data_to_save.append(f"Производитель: {motherboard.Manufacturer}")
        data_to_save.append(f"Модель: {motherboard.Product}")
        data_to_save.append(f"Серийный номер: {motherboard.SerialNumber}\n")
    
    for processor in c.Win32_Processor():
        data_to_save.append("Процессор:")
        data_to_save.append(f"Имя: {processor.Name}")
        data_to_save.append(f"Производитель: {processor.Manufacturer}")
        data_to_save.append(f"Ядра: {processor.NumberOfCores}")
        data_to_save.append(f"Потоки: {processor.NumberOfLogicalProcessors}")
        data_to_save.append(f"Частота: {processor.MaxClockSpeed} МГц\n")

    for memory in c.Win32_PhysicalMemory():
        data_to_save.append("Память:")
        data_to_save.append(f"Объем: {int(memory.Capacity) / 1048576:.2f} Mb")
        device_id = memory.Manufacturer
        data_to_save.append(f"ID: {device_id}")
        vendor_name = get_vendor_name(device_id)
        data_to_save.append(f"Производитель: {vendor_name}")
        data_to_save.append(f"Серийный номер: {memory.SerialNumber.strip()}")
        memory_type = memory.MemoryType
        if memory_type == "Неизвестно":
            data_to_save.append(f"Тип (не понятно добавь инфу в memory_types.json): {memory.MemoryType}")
        else:
            data_to_save.append(f"Тип: {get_ddr_type(memory_type)}")
        data_to_save.append(f"Частота: {memory.Speed} МГц\n")

    for disk in c.Win32_DiskDrive():
        data_to_save.append("Хард диск:")
        data_to_save.append(f"Модель: {disk.Model}")
        data_to_save.append(f"Серийный номер: {disk.SerialNumber.strip()}")
        data_to_save.append(f"Размер: {int(disk.Size) / (1024 ** 3):.2f} ГБ\n")

    for gpu in c.Win32_VideoController():
        data_to_save.append("Видеокарта:")
        data_to_save.append(f"Модель: {gpu.Name}")
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    reports_dir = os.path.join(script_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    file_path = os.path.join(reports_dir, f"hardware_info_{current_computer}.txt")

    save_to_file(data_to_save, file_path)

    return file_path, data_to_save
