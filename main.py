import subprocess

client_count = 1

python_interpreter = "C:/Users/emmet/AppData/Local/Programs/Python/Python39/python.exe"

script1 = 'server.py'
script2 = 'client.py'

subprocess.Popen(f'start cmd /k {python_interpreter} {script1}', shell=True)

for i in range(client_count):
    subprocess.Popen(f'start cmd /k {python_interpreter} {script2}', shell=True)
    sleep = 2