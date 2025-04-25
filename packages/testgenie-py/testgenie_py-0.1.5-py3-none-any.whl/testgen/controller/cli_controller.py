import argparse
import inspect
import os
import sys

import docker
from docker import DockerClient
from docker import errors

from testgen.controller.docker_controller import DockerController
from testgen.service.service import Service
from testgen.presentation.cli_view import CLIView
from testgen.sqlite.db_service import DBService

AST_STRAT = 1
FUZZ_STRAT = 2
RANDOM_STRAT = 3
REINFORCE_STRAT = 4

UNITTEST_FORMAT = 1
PYTEST_FORMAT = 2
DOCTEST_FORMAT = 3

class CLIController:
    #TODO: Possibly create a view 'interface' and use dependency injection to extend other views
    def __init__(self, service: Service, view: CLIView):
        self.service = service
        self.view = view

    def run(self):
        parser = argparse.ArgumentParser(description="A CLI tool for generating unit tests.")
        parser.add_argument("file_path", type=str, help="Path to the Python file.")
        parser.add_argument("--output", "-o", type=str, help="Path to output directory.")
        parser.add_argument(
            "--generate-only", "-g",
            action="store_true",
            help="Generate branched code but skip running unit tests and coverage."
        )
        parser.add_argument(
            "--test-mode",
            choices=["ast", "random", "fuzz", "reinforce"],
            default="ast",
            help="Set the test generation analysis technique"
        )
        parser.add_argument(
            "--reinforce-mode",
            choices=["train", "collect"],
            default="train",
            help="Set mode for reinforcement learning"
        )
        parser.add_argument(
            "--test-format",
            choices=["unittest", "pytest", "doctest"],
            default="unittest",
            help="Set the test generation format"
        )
        parser.add_argument(
            "--safe",
            action="store_true",
            help="Run test generation from within a docker container."
        )
        parser.add_argument(
            "--db",
            type=str,
            default="testgen.db",
            help="Path to SQLite database file (default: testgen.db)"
        )
        parser.add_argument(
            "--select-all",
            action="store_true",
            help="Select all from sqlite db"
        )
        parser.add_argument(
            "--visualize",
            action="store_true",
            help = "Visualize the tests with graphviz"
        )

        args = parser.parse_args()

        if args.select_all:
            self.view.display_message("Selecting all from SQLite database...")
            # Assuming you have a method in your service to handle this
            self.service.select_all_from_db()
            return
        
        # Initialize database service with specified path
        if hasattr(args, 'db') and args.db:
            self.service.db_service = DBService(args.db)
            self.view.display_message(f"Using database: {args.db}")
            
        running_in_docker = os.environ.get("RUNNING_IN_DOCKER") is not None
        if running_in_docker:
            args.file_path = self.adjust_file_path_for_docker(args.file_path)
            self.execute_generation(args)
        elif args.safe and not running_in_docker:
            client = self.docker_available()
            # Skip Docker-dependent operations if client is None
            if client is None and args.safe:
                self.view.display_message("Running with --safe flag requires Docker. Continuing without safe mode.")
                args.safe = False
            docker_controller = DockerController()
            project_root = self.get_project_root_in_docker(args.file_path)
            successful: bool = docker_controller.run_in_docker(project_root, client, args)
            if not successful:
                self.execute_generation(args)
        else:
            self.view.display_message("Running in local mode...")
            self.execute_generation(args)

    def execute_generation(self, args: argparse.Namespace):
        try:
            self.service.set_file_path(args.file_path)
            if args.test_format == "pytest":
                self.service.set_test_generator_format(PYTEST_FORMAT)
            elif args.test_format == "doctest":
                self.service.set_test_generator_format(DOCTEST_FORMAT)
            else:
                self.service.set_test_generator_format(UNITTEST_FORMAT)
            if args.test_mode == "random":
                self.view.display_message("Using Random Feedback-Directed Test Generation Strategy.")
                self.service.set_test_analysis_strategy(RANDOM_STRAT)
            elif args.test_mode == "fuzz":
                self.view.display_message("Using Fuzz Test Generation Strategy...")
                self.service.set_test_analysis_strategy(FUZZ_STRAT)
            elif args.test_mode == "reinforce":
                self.view.display_message("Using Reinforcement Learning Test Generation Strategy...")
                if args.reinforce_mode == "train":
                    self.view.display_message("Training mode enabled - will update Q-table")
                else:
                    self.view.display_message("Training mode disabled - will use existing Q-table")
                self.service.set_test_analysis_strategy(REINFORCE_STRAT)
                self.service.set_reinforcement_mode(args.reinforce_mode)
            else:
                self.view.display_message("Generating function code using AST analysis...")
                generated_file_path = self.service.generate_function_code()
                self.view.display_message(f"Generated code saved to: {generated_file_path}")
                if not args.generate_only:
                    self.view.display_message("Using Simple AST Traversal Test Generation Strategy...")
                    self.service.set_test_analysis_strategy(AST_STRAT)

            test_file = self.service.generate_tests(args.output)
            self.view.display_message(f"Unit tests saved to: {test_file}")
            self.view.display_message("Running coverage...")
            self.service.run_coverage(test_file)
            self.view.display_message("Tests and coverage data saved to database.")

            if args.visualize:
                self.service.visualize_test_coverage()

        except Exception as e:
            self.view.display_error(f"An error occurred: {e}")
            # Make sure to close the DB connection on error
            if hasattr(self.service, 'db_service'):
                self.service.db_service.close()

    def adjust_file_path_for_docker(self, file_path) -> str:
        file_dir = os.path.abspath(os.path.dirname(file_path))
        sys.path.append(file_dir)
        sys.path.append('/controller')
        file_abs_path = os.path.abspath(file_path)
        if not os.path.exists(file_abs_path):
            testgen_path = os.path.join('/controller/testgen', os.path.basename(file_path))
            if os.path.exists(testgen_path):
                file_path = testgen_path
            else:
                app_path = os.path.join('/controller', os.path.basename(file_path))
                if os.path.exists(app_path):
                    file_path = app_path
        return file_path

    def get_project_root_in_docker(self, script_path) -> str:
        script_path = os.path.abspath(sys.argv[0])
        print(f"Script path: {script_path}")
        script_dir = os.path.dirname(script_path)
        print(f"Script directory: {script_dir}")
        project_root = os.path.dirname(script_dir)
        print(f"Project root directory: {project_root}")
        return project_root

    def docker_available(self) -> DockerClient | None:
        try:
            client = docker.from_env()
            client.ping()
            self.view.display_message("Docker daemon is running and connected.")
            return client
        except docker.errors.DockerException as err:
            print(f"Docker is not available: {err}")
            print(f"Make sure the Docker daemon is running, and try again.")
            choice = input("Continue without Docker (y/n)?")
            if choice.lower() == 'y':
                return None
            else:
                sys.exit(1)
