import inspect
import os

from AuxFunctions import to_title_case_label, to_camel_case


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

