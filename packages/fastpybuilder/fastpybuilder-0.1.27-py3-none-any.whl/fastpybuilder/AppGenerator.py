import inspect
import os

from AuxFunctions import to_title_case_label, to_camel_case


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

