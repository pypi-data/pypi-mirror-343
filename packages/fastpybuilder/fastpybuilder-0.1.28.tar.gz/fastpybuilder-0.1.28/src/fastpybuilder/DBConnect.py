"""

This class is specific to manage the pre generation while first execution when the db info is set on its constructor,
is pretty important to not change the code of any python file in this project, doing it without the entire knowledgment
of how it is connected would cause failures in it execution.
This project is created to help lower dessertion fron system students in my university, also for fun,
and at the same time, to help others make their backend projects faster.

"""


import re
import string
import inspect
import os

def to_camel_case(text):
    parts = text.replace('_', ' ').split()
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])



def to_title_case_label(text):

    clean = re.sub(r"[_\-]+", " ", text)

    clean = re.sub(r"\s+", " ", clean).strip()

    return string.capwords(clean).replace(" ","")

class AppGenerator:

    def generate(self, variables: dict):
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        ruta_absoluta = os.path.abspath(caller_file)
        ruta_absoluta = str(ruta_absoluta).replace('DBConnect.py','')
        ruta_relativa = os.path.relpath(ruta_absoluta)

        path = os.path.join(f"{ruta_absoluta}/", f"App.py")
        with open(path, "w") as f:
            text = "import Ejecutar\nfrom controller import *\ntry:\n    from flask import Flask, request, jsonify, render_template\n    app = Flask(__name__)\n"
            f.write(text)

        for key in variables:
            print(key, variables[key])
            path = os.path.join(f"{ruta_absoluta}/", f"App.py")
            with open(path, "a") as f:
                f.write(f"    app.register_blueprint({to_camel_case(str(key))}, url_prefix='/{to_camel_case(str(key))}')\n")

        path = os.path.join(f"{ruta_absoluta}/", f"App.py")
        with open(path, "a") as f:
            text = """
    if __name__ == "__main__":
        print(" Starting FastPyBuilder Project Backend")
        app.run(debug=True)
except Exception as e:
    Ejecutar.inicioEjecucion()"""
            f.write(text)


class ControllersGenerator:

    def generate(self, variables: dict):
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        ruta_absoluta = os.path.abspath(caller_file)
        ruta_absoluta = str(ruta_absoluta).replace('DBConnect.py','')
        ruta_relativa = os.path.relpath(ruta_absoluta)
        print('ruta absoluta: ', ruta_absoluta)
        print('ruta relativa: ', ruta_relativa)
        os.makedirs(f"{ruta_absoluta}/controller", exist_ok=True)

        for key in variables:
            print(key, variables[key])
            path = os.path.join(f"{ruta_absoluta}/controller", f"__init__.py")
            with open(path, "a") as f:
                f.write(f"from .{to_title_case_label(str(key))}Controller import {to_camel_case(str(key))}\n")
            path = os.path.join(f"{ruta_absoluta}/controller", f"{to_title_case_label(str(key))}Controller.py")
            with open(path, "w") as f:
                text = f"""
from flask import Blueprint, request
from service import {to_title_case_label(str(key))}Service

{to_camel_case(str(key))} = Blueprint('{to_camel_case(str(key))}', __name__)
{to_camel_case(str(key))}Service = {to_title_case_label(str(key))}Service()

@{to_camel_case(str(key))}.route('/getAll', methods=['GET'])
def getAll():
    return {to_camel_case(str(key))}Service.getAll()

@{to_camel_case(str(key))}.route('/getid/<int:id>', methods=['GET'])
def getid(id):
    return {to_camel_case(str(key))}Service.getId(id)

@{to_camel_case(str(key))}.route('/save', methods=['POST'])
def save():
    return {to_camel_case(str(key))}Service.save(request.get_json())

@{to_camel_case(str(key))}.route('/update', methods=['PUT'])
def update():
    return {to_camel_case(str(key))}Service.update(request.get_json())

@{to_camel_case(str(key))}.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    return {to_camel_case(str(key))}Service.delete(id)"""
                f.write(text)



dictsRelationPsql = {
    'integer': 'Integer',
    'character varying': 'String',
    'bytea': 'LargeBinary',
    'timestamp without time zone': 'DateTime',
    'text': 'Text'
}

class ModelsGenerator:

    def generate(self, variables: dict):
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        ruta_absoluta = os.path.abspath(caller_file)
        ruta_absoluta = str(ruta_absoluta).replace('DBConnect.py','')
        ruta_relativa = os.path.relpath(ruta_absoluta)
        os.makedirs(f"{ruta_absoluta}/model", exist_ok=True)

        for key in variables:
            print(key, variables[key])
            path = os.path.join(f"{ruta_absoluta}/model", f"__init__.py")
            with open(path, "a") as f:
                f.write(f"from .{to_title_case_label(str(key))} import {to_title_case_label(str(key))}\n")
            path = os.path.join(f"{ruta_absoluta}/model", f"{to_title_case_label(str(key))}.py")
            with open(path, "w") as f:
                text = f"""
from repository.Connector import Base
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    SmallInteger,
    Float,
    Numeric,
    String,
    Text,
    Boolean,
    Date,
    Time,
    DateTime,
    Interval,
    Enum,
    LargeBinary,
    JSON,
)
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    JSONB,
    UUID,
    INET,
    MACADDR,
    MONEY,
    BYTEA,
    TSVECTOR,
)

class {to_title_case_label(str(key))}(Base):
    __tablename__ = "{str(key)}"\n
"""
                f.write(text)
        for key in variables:
            path = os.path.join(f"{ruta_absoluta}/model", f"{to_title_case_label(str(key))}.py")
            for data in variables[key]:
                print(key, variables[key])
                with open(path, "a") as f:
                    if data[0] != 'id':
                        text = f"    {data[0]} = Column({dictsRelationPsql[data[1]]})\n"
                    else:
                        text = f"    {data[0]} = Column({dictsRelationPsql[data[1]]}, primary_key=True)\n"
                    f.write(text)



class RepositorysGenerator:

    def generate(self, variables: dict, user:str, password:str, host:str, port:int,dbname:str):
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        ruta_absoluta = os.path.abspath(caller_file)
        ruta_absoluta = str(ruta_absoluta).replace('DBConnect.py','')
        ruta_relativa = os.path.relpath(ruta_absoluta)
        os.makedirs(f"{ruta_absoluta}/repository", exist_ok=True)

        for key in variables:
            print(key, variables[key])
            path = os.path.join(f"{ruta_absoluta}/repository", f"__init__.py")
            with open(path, "a") as f:
                f.write(f"from .{to_title_case_label(str(key))}Repository import {to_title_case_label(str(key))}Repository\n")
            path = os.path.join(f"{ruta_absoluta}/repository", f"{to_title_case_label(str(key))}Repository.py")
            with open(path, "w") as f:
                text = f"""
import json
from RepositoryAnnotation import RepositoryAnnotation
from repository.Connector import SessionLocal

@RepositoryAnnotation(model_class_path='model.{to_title_case_label(str(key))}.{to_title_case_label(str(key))}', session_local=SessionLocal)
class {to_title_case_label(str(key))}Repository:
    pass"""
                f.write(text)
        path = os.path.join(f"{ruta_absoluta}/repository", f"Connector.py")
        with open(path, "a") as f:
            text = f"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine(
    'postgresql+psycopg2://{user}:{password}@{host}:{str(port)}/{dbname}')
SessionLocal = sessionmaker(autocommit=False, bind=engine)
Base.metadata.create_all(engine)"""
            f.write(text)


class ServicesGenerator:

    def generate(self, variables: dict):
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        ruta_absoluta = os.path.abspath(caller_file)
        ruta_absoluta = str(ruta_absoluta).replace('DBConnect.py','')
        ruta_relativa = os.path.relpath(ruta_absoluta)
        os.makedirs(f"{ruta_absoluta}/service", exist_ok=True)

        for key in variables:
            print(key, variables[key])
            path = os.path.join(f"{ruta_absoluta}/service", f"__init__.py")
            with open(path, "a") as f:
                f.write(f"from .{to_title_case_label(str(key))}Service import {to_title_case_label(str(key))}Service\n")
            path = os.path.join(f"{ruta_absoluta}/service", f"{to_title_case_label(str(key))}Service.py")
            with open(path, "w") as f:
                text = f"""
import json

from model import {to_title_case_label(str(key))}
from repository import {to_title_case_label(str(key))}Repository

class {to_title_case_label(str(key))}Service:

    def __init__(self):
        self.repository = {to_title_case_label(str(key))}Repository()


    def save(self, {to_camel_case(str(key))}):
        obj = {to_title_case_label(str(key))}()
        for key, value in {to_camel_case(str(key))}.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return json.dumps(vars(self.repository.save(obj)))


    def delete(self, id):
        return {str("{'id eliminado': self.repository.delete(id)}")}

    def update(self, {to_camel_case(str(key))}):
        obj = {to_title_case_label(str(key))}()
        for key, value in {to_camel_case(str(key))}.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return json.dumps(vars(self.repository.update(obj)))

    def getId(self, id):
        return json.dumps(vars(self.repository.getId(id)))

    def getAll(self):
        data = [json.dumps(vars(objeto)) for objeto in self.repository.getAll()]
        parsed_data = [json.loads(item) for item in data]
        return json.dumps(parsed_data, indent=4)"""
                f.write(text)



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



try:
    import subprocess
    import platform
    import os
    import socket
    import psycopg2
    import mysql.connector
except Exception as e:
    print("You have not installed the requested packages.")


class DBConnect:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.system = platform.system()
        self.dbtype = None
        self.dbtype = self.__getDBtype()



    def __getDBtype(self):

        try:
            subprocess.run(['psql', '--version'], capture_output=True, text=True, check=True)
            print("✔️ psql está instalado.")
        except FileNotFoundError:
            print("❌ psql is not installed or in the classpath")



        try:
            subprocess.run(['mysql', '--version'], capture_output=True, text=True, check=True)
            print("✔️ mysql está instalado.")
        except FileNotFoundError:
            print("❌ mysql is not installed or in the classpath")


        try:

            with socket.create_connection((self.host, self.port), timeout=2):
                pass
        except Exception as e:
            print(e)
            print("No se puede conectar al host o puerto")


        env_pg = os.environ.copy()
        env_pg['PGPASSWORD'] = self.password

        pg_cmd = [
            'psql',
            '-h', self.host,
            '-U', self.user,
            '-d', self.dbname,
            '-p', str(self.port),
            '-c', 'SELECT version();'
        ]

        try:
            result = subprocess.run(pg_cmd, capture_output=True, text=True, env=env_pg, timeout=2)
            if result.returncode == 0 and "PostgreSQL" in result.stdout:
                self.dbtype = "psql"
        except Exception as e:
            print("Fail: Could not connect through PostgreSQL")

        # Probar MySQL
        env_my = os.environ.copy()
        env_my['MYSQL_PWD'] = self.password

        mysql_cmd = [
            'mysql',
            '-h', self.host,
            '-u', self.user,
            '-P', str(self.port),
            self.dbname,
            '-e', 'SELECT VERSION();',
            '--connect-timeout=5'
        ]

        try:
            result = subprocess.run(mysql_cmd, capture_output=True, text=True, env=env_my, timeout=2)
            if result.returncode == 0 and "VERSION()" in result.stdout:
                self.dbtype = "mysql"
        except Exception as e:
            print("Fail: Could not connect through MySql")

        print("Detected Database: ",self.dbtype)
        self.__startGenerator()

    def __startGenerator(self):
        print("Starting Generator")
        if self.dbtype == 'psql':
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )

            cur = conn.cursor()
            cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position
            """)

            entities = cur.fetchall()
            dict = {}
            for keys in [i[0] for i in entities]:
                dict[keys] = []
            for row in entities:
                dict[row[0]].append((row[1], row[2]))

            cur.close()         # En MySQL, table_schema es el nombre de la base de datos
            conn.close()
            ModelsGenerator().generate(dict)
            RepositorysGenerator().generate(dict, self.user, self.password, self.host, self.port, self.dbname)
            ServicesGenerator().generate(dict)
            ControllersGenerator().generate(dict)
            AppGenerator().generate(dict)
            BatsGenerator().generate(dict)
            print("----------------------------------------------------------------")
            print("----------------------------------------------------------------")
            print("          PROJECT GENERATED WITH FASTPYBUILDER                  ")
            print("             By Lenin Ospina Lamprea                            ")
            print("              Medellin's University                             ")
            print("----------------------------------------------------------------")
            print("----------------------------------------------------------------")