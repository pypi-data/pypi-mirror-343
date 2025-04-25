from typing import List
from testgen.tree.node import Node

class CodeGenerator:
    def __init__(self):
        pass

    def generate_code_from_tree(self, func_name: str, root: Node, params: List[str], operation, is_class_method: bool) -> str:
        def traverse(node, depth, path=[], indent_level=1):
            base_indent = "    " * indent_level

            if depth == len(params):
                path = path + [node.value]
                if is_class_method:
                    result = operation(self, *path)
                else:
                    result = operation(*path)
                if isinstance(result, str):
                    return f"{base_indent}return '{result}'\n"
                else:
                    return f"{base_indent}return {result}\n"

            param = params[depth]

            if isinstance(node.value, bool):
                path = path + [node.value]

            true_branch = f"{base_indent}if {param} == True:\n"
            false_branch = f"{base_indent}else:\n"

            true_code = traverse(node.children[0], depth + 1, path, indent_level + 1)
            false_code = traverse(node.children[1], depth + 1, path, indent_level + 1)

            return f"{true_branch}{true_code}{false_branch}{false_code}"

        typed_param_list = []
        if is_class_method:
            typed_param_list.append("self")

        for param in params:
            typed_param_list.append(f"{param}: bool")

        #TODO: Change this so it only adds self to classes rather than scripts
        function_code = f"def {func_name}({', '.join(typed_param_list)}):\n"
        body_code = traverse(root, 0)

        return function_code + body_code

    def generate_class(self, class_name):
        branched_class_name = f"Generated{class_name}"
        file_path = f"generated_{class_name.lower()}.py"
        class_file = open(f"{file_path}", "w")
        class_file.write(f"class {branched_class_name}:\n")
        return class_file

    """def generate_all_functions_code(self, class_name, operation):
        functions = self.inspect_class(class_name)
        trees = self.build_func_trees(functions)
        all_functions_code = {}

        for func, root, params in trees:
            code = self.generate_code_from_tree(root, params, operation)
            all_functions_code[func.__name__] = code
            print(f"Generated code for function '{func.__name__}':\n{code}\n")

        return all_functions_code"""