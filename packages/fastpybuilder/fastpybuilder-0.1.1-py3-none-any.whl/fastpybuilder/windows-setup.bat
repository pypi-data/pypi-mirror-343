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
call fastPyBuilderVenv\Scripts\activate

:: Instalar dependencias desde requirements.txt
pip install -r requirements.txt

:: Mensaje de éxito
echo --------------------------------------------------------------------------------------
echo ✅ Entorno virtual creado e instalado con éxito.
echo Backend de Python con SQLAlchemy para PostgreSQL por Lenin Ospina Lamprea, MIT License.

