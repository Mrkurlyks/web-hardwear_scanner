import os

def cliner():
    try:
        current_dir = os.getcwd()
        files = os.listdir(current_dir)
        for file in files:
            if file.endswith(".txt"):
                os.remove(os.path.join(current_dir, file))
                print(f"Файл {file} успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении файлов: {e}")