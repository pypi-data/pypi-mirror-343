import inspect
import os

from AuxFunctions import to_title_case_label, to_camel_case

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




