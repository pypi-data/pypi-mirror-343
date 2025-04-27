"""

This class is specific to manage the pre generation while first execution when the db info is set on its constructor,
is pretty important to not change the code of any python file in this project, doing it without the entire knowledgment
of how it is connected would cause failures in it execution.
This project is created to help lower dessertion fron system students in my university, also for fun,
and at the same time, to help others make their backend projects faster.

"""






import Ejecutar
from AppGenerator import AppGenerator
from ControllersGenerator import ControllersGenerator
from ModelsGenerator import ModelsGenerator
from RepositoryGenerator import RepositorysGenerator
from ServicesGenerator import ServicesGenerator

try:
    import subprocess
    import platform
    import os
    import socket
    import psycopg2
    import mysql.connector
except Exception as e:
    Ejecutar.inicioVenv()

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

            print("----------------------------------------------------------------")
            print("----------------------------------------------------------------")
            print("          PROJECT GENERATED WITH FASTPYBUILDER                  ")
            print("             By Lenin Ospina Lamprea                            ")
            print("              Medellin's University                             ")
            print("----------------------------------------------------------------")
            print("----------------------------------------------------------------")

            Ejecutar.inicioEjecucion()
"""
        if self.dbtype == 'mysql':
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbname
            )

            cur = conn.cursor()

            cur.execute(f"
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = '{self.dbname}'
                ORDER BY table_name, ordinal_position
            ")
            entities = cur.fetchall()
            dict = {}
            for keys in [i[0] for i in entities]:
                dict[keys] = []
            for row in entities:
                dict[row[0]].append((row[1], row[2]))

            cur.close()
            conn.close()

            ControllersGenerator().generate(dict)"""




DBConnect(host='aws-0-us-east-2.pooler.supabase.com',
          port=6543,
          dbname='postgres',
          user= 'postgres.ywswwkqspwwewemckxsx',
          password='PDw2EVsDIg2uZtzf')