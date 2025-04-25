import ast
from typing import List

import z3

import testgen.util.file_utils
from testgen.models.test_case import TestCase
from testgen.util.z3_utils import ast_to_z3
from testgen.util.z3_utils.constraint_extractor import extract_branch_conditions


def solve_branch_condition(file_name: str, func_node: ast.FunctionDef, uncovered_lines: List[int]) -> List[TestCase]:
    branch_conditions, param_types = extract_branch_conditions(func_node)
    uncovered_conditions = [bc for bc in branch_conditions if bc.line_number in uncovered_lines]
    test_cases = []

    for branch_condition in uncovered_conditions:
        z3_expr, z3_vars = ast_to_z3.ast_to_z3_constraint(branch_condition, param_types)
        solver = z3.Solver()
        solver.add(z3_expr)

        if solver.check() == z3.sat:
            model = solver.model()

            # Create default values for all parameters
            param_values = {}
            for param_name in param_types:
                # Set default values based on type
                if param_types[param_name] == "int":
                    param_values[param_name] = 0
                elif param_types[param_name] == "float":
                    param_values[param_name] = 0.0
                elif param_types[param_name] == "bool":
                    param_values[param_name] = False
                elif param_types[param_name] == "str":
                    param_values[param_name] = ""
                else:
                    param_values[param_name] = None

            # Update with model values where available
            for var_name, z3_var in z3_vars.items():
                if var_name in param_types and z3_var in model:
                    try:
                        if param_types[var_name] == "int":
                            param_values[var_name] = model[z3_var].as_long()
                        elif param_types[var_name] == "float":
                            param_values[var_name] = float(model[z3_var].as_decimal())
                        elif param_types[var_name] == "bool":
                            param_values[var_name] = z3.is_true(model[z3_var])
                        elif param_types[var_name] == "str":
                            param_values[var_name] = str(model[z3_var])
                        else:
                            param_values[var_name] = model[z3_var].as_long()
                    except Exception as e:
                        print(f"Error converting Z3 model value for {var_name}: {e}")

            # Ensure all parameters are included in correct order
            ordered_params = []
            for arg in func_node.args.args:
                arg_name = arg.arg
                if arg_name == 'self':  # Skip self parameter for class methods
                    continue
                if arg_name in param_values:
                    ordered_params.append(param_values[arg_name])
                else:
                    print(f"Warning: Missing value for parameter {arg_name}")
                    # Provide default values based on annotation if available
                    if hasattr(arg, 'annotation') and arg.annotation:
                        if isinstance(arg.annotation, ast.Name):
                            if arg.annotation.id == 'int':
                                ordered_params.append(0)
                            elif arg.annotation.id == 'float':
                                ordered_params.append(0.0)
                            elif arg.annotation.id == 'bool':
                                ordered_params.append(False)
                            elif arg.annotation.id == 'str':
                                ordered_params.append('')
                            else:
                                ordered_params.append(None)
                        else:
                            ordered_params.append(None)
                    else:
                        ordered_params.append(None)

            func_name = func_node.name
            try:
                module = testgen.util.file_utils.load_module(file_name)
                func = getattr(module, func_name)
                result = func(*ordered_params)
                test_cases.append(TestCase(func_name, tuple(ordered_params), result))
            except Exception as e:
                print(f"Error executing function with Z3 solution for {func_name}: {e}")

    return test_cases