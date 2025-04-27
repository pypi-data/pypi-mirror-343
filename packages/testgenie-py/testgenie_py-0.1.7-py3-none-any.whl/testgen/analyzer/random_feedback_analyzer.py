import ast
import importlib
import random
import time
import traceback
from typing import List, Dict, Set

import testgen.util.randomizer
import testgen.util.utils as utils
import testgen.util.coverage_utils as coverage_utils
from testgen.analyzer.contracts.contract import Contract
from testgen.analyzer.contracts.no_exception_contract import NoExceptionContract
from testgen.analyzer.contracts.nonnull_contract import NonNullContract
from testgen.models.test_case import TestCase
from testgen.analyzer.test_case_analyzer import TestCaseAnalyzerStrategy
from abc import ABC

from testgen.models.function_metadata import FunctionMetadata


# Citation in which this method and algorithm were taken from:
# C. Pacheco, S. K. Lahiri, M. D. Ernst and T. Ball, "Feedback-Directed Random Test Generation," 29th International
# Conference on Software Engineering (ICSE'07), Minneapolis, MN, USA, 2007, pp. 75-84, doi: 10.1109/ICSE.2007.37.
# keywords: {System testing;Contracts;Object oriented modeling;Law;Legal factors;Open source software;Software
# testing;Feedback;Filters;Error correction codes},

class RandomFeedbackAnalyzer(TestCaseAnalyzerStrategy, ABC):
    def __init__(self, analysis_context=None):
        super().__init__(analysis_context)
        self.test_cases = []
        self.covered_lines: Dict[str, Set[int]] = {}

    # Algorithm described in above article
    # Classes is the classes for which we want to generate sequences
    # Contracts express invariant properties that hold both at entry and exit from a call
        # Contract takes as input the current state of the system (runtime values created in the sequence so far, and any exception thrown by the last call), and returns satisfied or violated
        # Output is the runtime values and boolean flag violated
    # Filters determine which values of a sequence are extensible and should be used as inputs
    def generate_sequences(self, function_metadata: List[FunctionMetadata], classes=None, contracts: List[Contract] = None, filters=None, time_limit=20):
        contracts = [NonNullContract(), NoExceptionContract()]
        error_seqs = [] # execution violates a contract
        non_error_seqs = [] # execution does not violate a contract

        functions = self._analysis_context.function_data
        start_time = time.time()
        while(time.time() - start_time) >= time_limit:
            # Get random function
            func = random.choice(functions)
            param_types: dict = func.params
            vals: dict = self.random_seqs_and_vals(param_types)
            new_seq = (func.function_name, vals)
            if new_seq in error_seqs or new_seq in non_error_seqs:
                continue
            outs_violated: tuple = self.execute_sequence(new_seq, contracts)
            violated: bool = outs_violated[1]
            # Create tuple of sequence ((func name, args), output)
            new_seq_out = (new_seq, outs_violated[0])
            if violated:
                error_seqs.append(new_seq_out)
            else:
                # Question: Should I use the failed contract to be the assertion in unit test??
                non_error_seqs.append(new_seq_out)
        return error_seqs, non_error_seqs

    def generate_sequences_new(self, contracts: List[Contract] = None, filters=None, time_limit=20):
        contracts = [NonNullContract(), NoExceptionContract()]
        error_seqs = []  # execution violates a contract
        non_error_seqs = []  # execution does not violate a contract

        functions = self._analysis_context.function_data.copy()
        start_time = time.time()

        while (time.time() - start_time) < time_limit:
            # Get random function
            func = random.choice(functions)
            param_types: dict = func.params
            vals: dict = self.random_seqs_and_vals(param_types)
            new_seq = (func.function_name, vals)

            if new_seq in [seq[0] for seq in error_seqs] or new_seq in [seq[0] for seq in non_error_seqs]:
                continue

            outs_violated: tuple = self.execute_sequence(new_seq, contracts)
            violated: bool = outs_violated[1]

            # Create tuple of sequence ((func name, args), output)
            new_seq_out = (new_seq, outs_violated[0])

            if violated:
                error_seqs.append(new_seq_out)

            else:
                non_error_seqs.append(new_seq_out)

            test_case = TestCase(new_seq_out[0][0], tuple(new_seq_out[0][1].values()), new_seq_out[1])
            self.test_cases.append(test_case)
            fully_covered = self.covered(func)
            if fully_covered:
                print(f"Function {func.function_name} is fully covered")
                functions.remove(func)

            if not functions:
                self.test_cases.sort(key=lambda tc: tc.func_name)
                print("All functions covered")
                break

        self.test_cases.sort(key=lambda tc: tc.func_name)
        return error_seqs, non_error_seqs


    def covered(self, func: FunctionMetadata) -> bool:
        if func.function_name not in self.covered_lines:
            self.covered_lines[func.function_name] = set()

        for test_case in [tc for tc in self.test_cases if tc.func_name == func.function_name]:
            analysis = coverage_utils.get_coverage_analysis(self._analysis_context.filepath, self._analysis_context.class_name,
                                                                         func.function_name, test_case.inputs)
            covered = coverage_utils.get_list_of_covered_statements(analysis)
            self.covered_lines[func.function_name].update(covered)

        executable_statements = self.get_all_executable_statements(func)

        return self.covered_lines[func.function_name] == executable_statements

    def execute_sequence(self, sequence, contracts: List[Contract]):
        """Execute a sequence and check contract violations"""
        func_name, args_dict = sequence
        args = tuple(args_dict.values())  # Convert dict values to tuple

        try:
            # Use module from analysis context if available
            module = self.analysis_context.module

            if self._analysis_context.class_name:
                cls = getattr(module, self._analysis_context.class_name, None)
                if cls is None:
                    raise AttributeError(f"Class '{self._analysis_context.class_name}' not found")
                obj = cls()  # Instantiate the class
                func = getattr(obj, func_name, None)

                import inspect
                sig = inspect.signature(func)
                param_names = [p.name for p in sig.parameters.values() if p.name != 'self']
            else:
                func = getattr(module, func_name, None)

                import inspect
                sig = inspect.signature(func)
                param_names = [p.name for p in sig.parameters.values()]

            # Create ordered arguments based on function signature
            ordered_args = []
            for name in param_names:
                if name in args_dict:
                    ordered_args.append(args_dict[name])

            # Check preconditions
            for contract in contracts:
                if not contract.check_preconditions(tuple(ordered_args)):
                    print(f"Preconditions failed for {func_name} with {tuple(ordered_args)}")
                    return None, True

            # Execute function with properly ordered arguments
            output = func(*ordered_args)
            exception = None

        except Exception as e:
            print(f"EXCEPTION IN RANDOM FEEDBACK: {e}")
            print(traceback.format_exc())
            output = None
            exception = e

        # Check postconditions
        for contract in contracts:
            if not contract.check_postconditions(tuple(ordered_args), output, exception):
                print(f"Postcondition failed for {func_name} with {tuple(ordered_args)}")
                return output, True

        return output, False
    

    # TODO: Currently only getting random vals of primitives, extend to sequences
    def random_seqs_and_vals(self, param_types, non_error_seqs=None):
        return self.generate_random_inputs(param_types)

    @staticmethod
    def extract_parameter_types(func_node):
        """Extract parameter types from a function node."""
        param_types = {}
        for arg in func_node.args.args:
            param_name = arg.arg
            if arg.annotation:
                param_type = ast.unparse(arg.annotation)
                param_types[param_name] = param_type
            else:
                if param_name != 'self':
                    param_types[param_name] = None
        return param_types

    @staticmethod
    def generate_random_inputs(param_types):
        """Generate inputs for fuzzing based on parameter types."""
        inputs = {}
        for param, param_type in param_types.items():
            if param_type == "int":
                random_integer = random.randint(1, 100)
                inputs[param] = random_integer
            if param_type == "bool":
                random_choice = random.choice([True, False])
                inputs[param] = random_choice
            if param_type == "float":
                random_float = random.random()
                inputs[param] = random_float
            # TODO: Random String and Random bytes; Random objects?
            if param_type == "str":
                inputs[param] = "abc"
            #elif param_type == "bytes":
            #    inputs[param] = fdp.ConsumeBytes(10)
            #else:
            #    inputs[param] = None
        return inputs

    def collect_test_cases(self, function_metadata: FunctionMetadata) -> List[TestCase]:
        """Collect test cases using random feedback technique"""
        error_seqs, non_error_seqs = self.generate_sequences_new()
        test_cases = []

        # Process error sequences
        if error_seqs:
            for error_seq in error_seqs:
                print("ERROR SEQ OUTPUT:", error_seq[1])
                test_cases.append(TestCase(error_seq[0][0], tuple(error_seq[0][1].values()), error_seq[1]))

        # Process non-error sequences
        if non_error_seqs:
            for non_error_seq in non_error_seqs:
                print("NON ERROR SEQ OUTPUT:", non_error_seq[1])
                test_cases.append(TestCase(non_error_seq[0][0], tuple(non_error_seq[0][1].values()), non_error_seq[1]))

        return self.test_cases

    def get_all_executable_statements(self, func: FunctionMetadata):
        """Get all executable statements including else branches"""
        import ast

        test_cases = [tc for tc in self.test_cases if tc.func_name == func.function_name]

        if not test_cases:
            print("Warning: No test cases available to determine executable statements")
            from testgen.util.randomizer import new_random_test_case
            temp_case = new_random_test_case(self._analysis_context.filepath, func.func_def)
            analysis = coverage_utils.get_coverage_analysis(self._analysis_context.filepath, self._analysis_context.class_name, func.function_name,
                                                                         temp_case.inputs)
        else:
            analysis = coverage_utils.get_coverage_analysis(self._analysis_context.filepath, self._analysis_context.class_name, func.function_name, test_cases[0].inputs)

        # Get standard executable lines from coverage.py
        executable_lines = list(analysis[1])

        # Parse the source file to find else branches
        with open(self._analysis_context.filepath, 'r') as f:
            source = f.read()

        # Parse the code
        tree = ast.parse(source)

        # Find our specific function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func.func_def.name:
                # Find all if statements in this function
                for if_node in ast.walk(node):
                    if isinstance(if_node, ast.If) and if_node.orelse:
                        # There's an else branch
                        if isinstance(if_node.orelse[0], ast.If):
                            # This is an elif - already counted
                            continue

                        # Get the line number of the first statement in the else block
                        # and subtract 1 to get the 'else:' line
                        else_line = if_node.orelse[0].lineno - 1

                        # Check if this is actually an else line (not a nested if)
                        with open(self._analysis_context.filepath, 'r') as f:
                            lines = f.readlines()
                            if else_line <= len(lines):
                                line_content = lines[else_line - 1].strip()
                                if line_content == "else:":
                                    if else_line not in executable_lines:
                                        executable_lines.append(else_line)

        return sorted(executable_lines)