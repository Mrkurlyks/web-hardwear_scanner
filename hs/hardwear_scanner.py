import wmi
import json
import os
import pythoncom

def get_vendor_name(device_id):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'pci_data.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            vendor_data = json.load(file)
            vendor = vendor_data.get(str(device_id), 1)
            if vendor == 1: return device_id
            return vendor 
    except None:
        return ("не найдена бд")

def get_ddr_type(memory_type):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'memory_types.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            memory_types = json.load(file)
            types = memory_types.get(str(memory_type), 1)
            if types == 1: return memory_type
            return memory_types.get(str(memory_type))
    except FileNotFoundError:
        return ("не найдена бд")
    
def run_script(remote_computer=None):
    pythoncom.CoInitialize()
    try:
        c = wmi.WMI(computer=remote_computer)
        
        data_to_save = []
    
        data_to_save.append(f"Имя компьютера: {remote_computer}\n")
        
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
            data_to_save.append(f"Объем: {int(memory.Capacity) / 1048576:.2f} MB")
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
            data_to_save.append(f"Модель: {gpu.Name}\n")
        
        return "\n".join(data_to_save)
    except Exception as e:
        return f"Произошла ошибка: {e}"
    finally:
        pythoncom.CoUninitialize()

def run_mini (remote_computer=None):
    pythoncom.CoInitialize()
    try:
        c = wmi.WMI(computer=remote_computer)
        
        mini_data_to_save = []
    
        mini_data_to_save.append(f"Имя компьютера: {remote_computer}\n")
        for processor in c.Win32_Processor():
            mini_data_to_save.append(f"Процессор: {processor.Name}, {processor.MaxClockSpeed} МГц\n")
        
        for memory in c.Win32_PhysicalMemory():
            device_id = memory.Manufacturer
            memory_type = memory.MemoryType
            mini_data_to_save.append(f"Память: {int(memory.Capacity) / 1048576:.2f} MB {memory.Speed} МГц {get_vendor_name(device_id)} {get_ddr_type(memory_type)} \n")
        for disk in c.Win32_DiskDrive():
            mini_data_to_save.append(f"Харрд: {disk.Model} {int(disk.Size) / (1024 ** 3):.2f} ГБ {disk.SerialNumber.strip()}\n")
     
        for gpu in c.Win32_VideoController():
            mini_data_to_save.append(f"Видеокарта: {gpu.Name}\n")
            
        return "\n".join(mini_data_to_save)
    except Exception as e:
        return f"Произошла ошибка скрипта: {e}"
    finally:
        pythoncom.CoUninitialize()