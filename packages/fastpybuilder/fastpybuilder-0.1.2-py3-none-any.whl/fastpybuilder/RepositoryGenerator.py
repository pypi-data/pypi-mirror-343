import inspect
import os

from AuxFunctions import to_title_case_label, to_camel_case


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

