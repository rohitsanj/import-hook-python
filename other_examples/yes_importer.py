from importlib.machinery import ModuleSpec


class YesImporter:
    def find_spec(self, fullname, *args):
        # Yes
        return ModuleSpec(fullname, self)

    def create_module(self, module_name):
        return None

    def exec_module(self, module):
        print("Yes." + f"\nHere's {module.__name__}")


import sys

sys.meta_path.append(YesImporter())
