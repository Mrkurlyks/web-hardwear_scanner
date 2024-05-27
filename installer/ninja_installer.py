import subprocess
import os
import logging
from flask import request

install_logger = logging.getLogger("installer")
install_handler = logging.FileHandler("install_log.log", encoding="utf-8")
install_logger.addHandler(install_handler)
install_logger.setLevel(logging.INFO)

def convert_to_network_path(file_path):
    drive_path = os.path.splitdrive(file_path)[0] 
    relative_path = file_path.replace(drive_path, '') 
    network_path = f'\\\\{os.environ["COMPUTERNAME"]}\\{drive_path}${relative_path}'
    network_path = network_path.replace(':', "")
    return network_path

def install_package(remote_computer, file_path):
    temp_directory = f'C\\TEMP\\'
    fail_way = f'\\C\\TEMP\\{os.path.basename(file_path)}'
    network_file_path = convert_to_network_path(file_path)
    client_ip = request.remote_addr
    start_install_msg = f"Установка файла {network_file_path} на компьютер {remote_computer} (c IP: {client_ip}) начата."
    install_logger.info(start_install_msg)
    
    command = f"""
    $session = New-PSSession -ComputerName {remote_computer};
    Invoke-Command -Session $session -ScriptBlock {{
        if (-Not (Test-Path -Path '{temp_directory}')) {{
            New-Item -Path '{temp_directory}' -ItemType Directory;
        }}
        Copy-Item -Path '{network_file_path}' -Destination '{temp_directory}';
        $process = Start-Process msiexec.exe -ArgumentList '/i', '{fail_way}', '/quiet', '/norestart' -Wait -PassThru;
        Remove-Item -Path '{fail_way}';
        return $process.ExitCode;
    }};
    Remove-PSSession -Session $session;
    """
    
    try:
        result = subprocess.run(['powershell.exe', '-Command', command], capture_output=True, text=True, check=True)

        if result.returncode == 0:
            success_msg = f"Установка файла {file_path} на компьютер {remote_computer} (IP: {client_ip}) успешно завершена."
            install_logger.info(success_msg)
            return ('Установка прошла успешно.')
        else:
            error_msg = f"Ошибка при установке файла {file_path} на компьютер {remote_computer} (IP: {client_ip}). Код возврата: {result.returncode}. Ошибка: {result.stderr}"
            install_logger.error(error_msg)
            return error_msg

    except subprocess.CalledProcessError as e:
        error_msg = f"Произошла ошибка при установке файла {file_path} на компьютер {remote_computer} (IP: {client_ip}): {e}. Код возврата: {e.returncode}."
        install_logger.error(error_msg)
        return error_msg
