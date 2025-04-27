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
echo "✅ Vistual enviroment succesfully executed."

