def RepositoryAnnotation(model_class_path: str, session_local):
    def wrapper(cls):
        import importlib

        def get_model_class():
            module_path, class_name = model_class_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)

        def save(self, poObject):
            import inspect
            print(f"Running: {inspect.currentframe().f_code.co_name} with FastPyBuilder")
            with session_local() as session:
                session.add(poObject)
                session.commit()
                model_class = get_model_class()
                poObject = session.query(model_class).filter(model_class.id == poObject.id).first()
                poObject.__delattr__('_sa_instance_state')
                return poObject

        def delete(self, id):
            import inspect
            print(f"Running: {inspect.currentframe().f_code.co_name} with FastPyBuilder")
            with session_local() as session:
                model_class = get_model_class()
                session.query(model_class).filter(model_class.id == id).delete()
                session.commit()
                return id

        def update(self, poObject2):
            import inspect
            print(f"Running: {inspect.currentframe().f_code.co_name} with FastPyBuilder")
            poObject2.__delattr__('_sa_instance_state')
            with session_local() as session:
                model_class = get_model_class()
                poObject = session.query(model_class).filter(model_class.id == poObject2.id).first()
                for key, value in poObject2.__dict__.items():
                    setattr(poObject, key, value)
                session.commit()
                poObject = session.query(model_class).filter(model_class.id == poObject.id).first()
                poObject.__delattr__('_sa_instance_state')
                return poObject

        def getId(self, id):
            import inspect
            print(f"Running: {inspect.currentframe().f_code.co_name} with FastPyBuilder")
            with session_local() as session:
                model_class = get_model_class()
                poObject = session.query(model_class).filter(model_class.id == id).first()
                poObject.__delattr__('_sa_instance_state')
                return poObject

        def getAll(self):
            import inspect
            print(f"Running: {inspect.currentframe().f_code.co_name} with FastPyBuilder")
            with session_local() as session:
                model_class = get_model_class()
                lista = session.query(model_class).all()
                for i in lista:
                    i.__delattr__('_sa_instance_state')
                return lista

        setattr(cls, 'save', save)
        setattr(cls, 'delete', delete)
        setattr(cls, 'update', update)
        setattr(cls, 'getId', getId)
        setattr(cls, 'getAll', getAll)

        return cls
    return wrapper