BLOCK_LIST = ["socket", "http"]


class BlockListFinder:
    def find_spec(self, fullname: str, *args):
        first_module = fullname.split(".")[0]  # Get the first module
        if first_module in BLOCK_LIST:
            raise PermissionError(f"Sorry boss, we can't import '{fullname}' for you")

        # Continue to actually import this module
        return None


import sys

sys.meta_path.insert(0, BlockListFinder())
