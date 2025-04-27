import inspect
import os

from AuxFunctions import to_title_case_label, to_camel_case


class BatsGenerator:

    def generate(self, variables: dict):
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        ruta_absoluta = os.path.abspath(caller_file)
        ruta_absoluta = str(ruta_absoluta).replace('DBConnect.py','')
        ruta_relativa = os.path.relpath(ruta_absoluta)

        path = os.path.join(f"{ruta_absoluta}/", f"Ejecutar.py")
        with open(path, "w") as f:
            text = """

def inicioEjecucion():
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.run(["windows-setup.bat"], shell=True)

    elif sistema == "Linux":
        subprocess.run(["bash", "linux-setup.sh"])

    else:
        print("Sistema no compatible.")
"""
            f.write(text)


            f.write(text)

            path = os.path.join(f"{ruta_absoluta}/", f"linux-setup.sh")
            with open(path, "w") as f:
                text = """
#!/bin/bash


sudo apt install postgresql-client-common

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not instaled, trying to install..."
    sudo apt update
    sudo apt install python3 python3-pip -y
    echo "Python3 and pip have been install."
else
    echo "Python3 were already installed."
fi

if ! command -v pip &> /dev/null
then
    echo "pip is not installed. trying to install pip..."
    sudo apt install python3-pip -y
    echo "pip have been install."
else
    echo "pip is already in your system."
fi
if [ -d "fastPyBuilderVenv" ]; then
    echo "Virtual enviroment already exist, loading venv..."
else
    # Crear el entorno virtual si no existe
    python3 -m venv fastPyBuilderVenv
    echo "Virtual enviroment created succesfully."
fi
source fastPyBuilderVenv/bin/activate
pip install -r requirements.txt
echo "---------------------------------------------------------------------------------------"
echo "✅ Virtual enviroment succesfully executed."
echo "---------------------------------------------------------------------------------------"
echo "Python Backend with SQLAlchemy to PostgreSQL by Lenin Ospina Lamprea."
echo "▶ Executing..."
echo "----------------------------"
echo "----------------------------------------------------------------"
echo "---------------------------------------------------------------------------------------------------------"
echo "             Running  FASTPYBUILDER   :D             "
echo "---------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------"
echo "-----------------------------"
python3 App.py
        """
                f.write(text)

            path = os.path.join(f"{ruta_absoluta}/", f"windows-setup.bat")
            with open(path, "w") as f:
                text = f"""
@echo off
:: Verificar si Python está instalado
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Python no está instalado. Redirigiendo a la pagina de instalación...
    start https://www.python.org/downloads/
    exit /b
)

:: Verificar si pip está instalado
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip no está instalado. Instalando pip...
    python -m ensurepip --upgrade
)

:: Verificar si el entorno virtual ya existe
if exist "fastPyBuilderVenv" (
    echo El entorno virtual ya existe. Activando el entorno...
) else (
    :: Crear entorno virtual si no existe
    python -m venv fastPyBuilderVenv
    echo Entorno virtual creado con éxito.
)

:: Activar el entorno virtual
{str(r'call fastPyBuilderVenv\Scripts\activate')}

:: Instalar dependencias desde requirements.txt
pip install -r requirements.txt

:: Mensaje de éxito
echo --------------------------------------------------------------------------------------
echo ✅ Entorno virtual creado e instalado con éxito.
echo Backend de Python con SQLAlchemy para PostgreSQL por Lenin Ospina Lamprea, MIT License.
:: Ejecutar la aplicación
echo ▶ Ejecutando: python App.py
echo ---------------------------------------------------------------------------------------
echo Python Backend with SQLAlchemy to PostgreSQL by Lenin Ospina Lamprea.
echo ▶ Executing...
echo ----------------------------
echo ----------------------------------------------------------------
echo ---------------------------------------------------------------------------------------------------------
echo              Running  FASTPYBUILDER   :D
echo ---------------------------------------------------------------------------------------------------------
echo ----------------------------------------------------------------
echo -----------------------------
python App.py
                        """
                f.write(text)

                path = os.path.join(f"{ruta_absoluta}/", f"requirements.txt")
                with open(path, "w") as f:
                    text = f"""
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.1.31
click==8.1.8
distro==1.9.0
Flask==3.1.0
flask-cors==5.0.1
greenlet==3.2.0
h11==0.14.0
httpcore==1.0.8
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.9.0
MarkupSafe==3.0.2
mysql-connector-python==9.3.0
openai==1.75.0
psycopg2-binary==2.9.10
pydantic==2.11.3
pydantic_core==2.33.1
sniffio==1.3.1
SQLAlchemy==2.0.40
tqdm==4.67.1
typing-inspection==0.4.0
typing_extensions==4.13.2
Werkzeug==3.1.3
                                """
                    f.write(text)

