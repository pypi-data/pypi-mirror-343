import subprocess
import platform

def inicioVenv():
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.run(["windows-setup.bat"], shell=True)
        print("Now you can run the DBConnect class")
    elif sistema == "Linux":
        subprocess.run(["bash", "linux-setup.sh"])
        print("-- Now you can run the DBConnect class. Use ' venvLoader/bin/activate ' first --")
    else:
        print("Sistema no compatible.")

def inicioEjecucion():
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.run(["windows-run.bat"], shell=True)

    elif sistema == "Linux":
        subprocess.run(["bash", "linux-run.sh"])

    else:
        print("Sistema no compatible.")

