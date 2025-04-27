import inspect
import os

from AuxFunctions import to_title_case_label, to_camel_case


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

