import os
from string import Template
import yaml
import subprocess
import logging
import platform
logger = logging.getLogger(__name__)


class FrameworkAPI:
    """
    FrameworkAPI: A class for managing and executing scripts based on YAML configurations.
    """

    def __init__(self, config_path, log_file=None):
        """
        Initialize the FrameworkAPI with a YAML configuration file and set up logging.

        Args:
            config_path (str): Path to the YAML configuration file.
            log_file (str): Path to the log file for error and debug messages.
        """
        self.config_path = config_path
        self.raw_config = self._load_config(raw=True)
        self.config = self._load_config()
        if log_file:
            self._setup_logging(log_file)

    def _setup_logging(self, log_file):
        """
        Set up the logging configuration.

        Args:
            log_file (str): Path to the log file.
        """
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True
        )
        logger.debug("Logging initialized.")

    def _load_config(self, raw=False):
        """
        Load and parse the YAML configuration file.

        Args:
            raw (bool): If True, return raw YAML configuration without resolving references.

        Returns:
            dict: Parsed configuration as a dictionary.
        """
        try:
            with open(self.config_path, 'r') as f:
                raw_config = yaml.safe_load(f)
            logger.debug(f"Configuration loaded from {self.config_path}.")
            if raw:
                return raw_config
            else:
                return self._resolve_references(raw_config)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise

    def _resolve_references(self, config):
        """
        Resolve cross-references in the YAML configuration using string templates.

        Args:
            config (dict): The raw YAML configuration.

        Returns:
            dict: Configuration with resolved references.
        """
        try:
            def resolve(obj, context=None):
                if context is None:
                    context = obj
                if isinstance(obj, dict):
                    return {k: resolve(v, context) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [resolve(item, context) for item in obj]
                elif isinstance(obj, str):
                    return Template(obj).safe_substitute(context)
                else:
                    return obj

            return resolve(config)
        except Exception as e:
            logger.error(f"Error resolving references in configuration: {e}")
            raise

    def merge(self, other, overwrite=True):
        """
        Merge configurations from another FrameworkAPI instance.

        Args:
            other (FrameworkAPI): Another FrameworkAPI instance whose config will be merged.
            overwrite (bool): If True, overwrite existing keys with the values from `other`.

        Returns:
            None
        """
        try:
            def recursive_merge(dict1, dict2):
                for key, value in dict2.items():
                    if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                        recursive_merge(dict1[key], value)
                    elif overwrite or key not in dict1:
                        dict1[key] = value

            if isinstance(other, FrameworkAPI):
                recursive_merge(self.config, other.config)
                logger.info("Configurations merged successfully.")
            else:
                raise TypeError("Argument must be an instance of FrameworkAPI")
        except Exception as e:
            logger.error(f"Error merging configurations: {e}")
            raise

    def run_script(self, script_name, background=False):
        """
        Execute a single script based on its configuration. Optionally run a specific function in the script.

        Args:
            script_name (str): Name of the script to execute (as defined in the configuration).

        Raises:
            KeyError: If the script name is not found in the configuration.
            ValueError: If the script path is not defined.
        """
        try:
            scripts = self.config.get('scripts', {})
            if script_name not in scripts:
                raise KeyError(
                    f"Script '{script_name}' not found in configuration.")

            script_info = scripts[script_name]
            script_path = script_info.get('path')
            if os.path.isabs(script_path):
                script_path = os.path.relpath(
                    script_path, os.getcwd())
            script_path = script_path.replace('\\', '/')
            function_name = script_info.get('function', None)
            args = script_info.get('args', {})

            if not script_path:
                raise ValueError(
                    f"Script path not defined for '{script_name}'.")

            if function_name:
                # Run a specific function in the script
                spath = script_path.rsplit('.', 1)[0].replace(
                    '\\', '.').replace('/', '.')
                args_ = ', '.join([f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in args.items()])
                ext = os.path.splitext(script_path)[-1].lower()
                if ext == '.py':
                    command = [
                        self._get_interpreter(script_path), "-c" f'import {spath} as f; f.{function_name}({args_})']
                elif ext == '.r':
                    command = [self._get_interpreter(script_path), "-e",
                               f'source("{script_path}"); {function_name}({args_})']
                elif ext == '.jl':
                    command = [self._get_interpreter(script_path), "-e",
                               f'include("{script_path}"); {function_name}({args_})']
            else:
                # Construct the command
                command = [self._get_interpreter(script_path), script_path]
                for key, value in args.items():
                    command.extend([f"--{key}", str(value)])

            logger.info(
                f"Executing script '{script_name}' with command: {command}")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            for line in process.stdout:
                print(line.decode('utf8').strip())
                logger.info(line.decode('utf8').strip())
            for line in process.stderr:
                logger.error(line.decode('utf8').strip())

            if not background:
                process.wait()
            if process.returncode != 0:
                logger.error(
                    f"Script '{script_name}' exited with code {process.returncode}.")
        except Exception as e:
            logger.error(f"Error executing script '{script_name}': {e}")
            raise

    def run_workflow(self, background=False):
        """
        Execute all scripts defined in the workflow in sequence.
        """
        try:
            workflow = self.config.get('workflow', [])
            for script_name in workflow:
                self.run_script(script_name, background=background)
            logger.info("Workflow executed successfully.")
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            raise

    @staticmethod
    def _get_interpreter(script_path):
        """
        Determine the interpreter for a given script based on its file extension.

        Args:
            script_path (str): Path to the script.

        Returns:
            str: The interpreter command (e.g., 'python', 'Rscript', 'julia').

        Raises:
            ValueError: If the file extension is unsupported.
        """
        ext = os.path.splitext(script_path)[-1].lower()
        system = platform.system()

        if ext == '.py':
            if system == 'Linux':
                return 'python3'
            elif system == 'Windows':
                return 'python'
            elif system == 'Darwin':  # macOS
                return 'python3'
            else:
                return 'python'
        elif ext == '.r':
            return 'Rscript'
        elif ext == '.jl':
            return 'julia'
        else:
            raise ValueError(
                f"Unsupported script type for file '{script_path}'.")
