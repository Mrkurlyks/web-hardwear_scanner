import subprocess

def install_package(remote_computer, file_path):
        command = [
            "powershell.exe",
            "-Command",
            f"""
            Enable-PSRemoting -ComputerName {remote_computer};
            Invoke-Command -Session $session -ScriptBlock {{
                Start-Process msiexec.exe -ArgumentList '/i', '{file_path}', '/quiet', '/norestart' -Wait
            }};
            Remove-PSSession -Session $session
            """
        ]

        # Запуск команды PowerShell
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Проверка кода возврата
        if result.returncode == 0:
            print("Установка прошла успешно.")
        else:
            print("Ошибка при установке.")
            print("Код возврата:", result.returncode)
            print("Вывод ошибки:", result.stderr)

        # Вывод информации об установке
        print("Вывод:", result.stdout)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример вызова функции
remote_computer = "RemoteComputerName"
msi_path = "C:\\path\\to\\your\\installer.msi"
install_msi_remotely(remote_computer, msi_path)