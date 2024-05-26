import subprocess
import os

def install_package(remote_computer, file_path):
    temp_directory = f'\\\\{remote_computer}\\C$\\TEMP\\'
    fail_way = f'\\\\{remote_computer}\\C$\\TEMP\\{os.path.basename(file_path)}'
    
    command = f"""
    $session = New-PSSession -ComputerName {remote_computer};
    Invoke-Command -Session $session -ScriptBlock {{
        if (-Not (Test-Path -Path '{temp_directory}')) {{
            New-Item -Path '{temp_directory}' -ItemType Directory;
        }}
        Copy-Item -Path '{file_path}' -Destination '{temp_directory}';
        $process = Start-Process msiexec.exe -ArgumentList '/i', '{fail_way}', '/quiet', '/norestart' -Wait -PassThru;
        Remove-Item -Path '{fail_way}';
        return $process.ExitCode;
    }};
    Remove-PSSession -Session $session;
    """
    
    try:
        result = subprocess.run(['powershell.exe', '-Command', command], capture_output=True, text=True, check=True)

        if result.returncode == 0:
            return ('Установка прошла успешно.')
        else:
            return("Ошибка при установке.",result.returncode, result.stderr)

    except subprocess.CalledProcessError as e:
        return(f"Произошла ошибка: {e} Код возврата: {e.returncode} ошибкa: {e.stderr}")
