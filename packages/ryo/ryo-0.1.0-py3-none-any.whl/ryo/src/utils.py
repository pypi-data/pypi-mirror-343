from pathlib import Path
import yaml
import os
import yamale
from yamale.validators import Validator, DefaultValidators
from yamale.schema import Schema
from yamale import YamaleError

class StepValidator(Validator):
    tag = 'step'

    def _is_valid(self, value):
        action_fields = {
            'commit_file': {
                'required': [],
                'optional': ['file_path', 'commit_msg']
            },
            'workflow_monitor': {
                'required': ['workflow_name'],
                'optional': ['show_workflow']
            },
            'approve_pull_request': {
                'required': ['target'],
                'optional': []
            }
        }

        action = value.get('action')
        if not action:
            self._errors.append("O campo 'action' é obrigatório.")
            return False

        if action not in action_fields:
            self._errors.append(f"A ação '{action}' não é reconhecida.")
            return False

        required_fields = action_fields[action]['required']
        optional_fields = action_fields[action]['optional']
        allowed_fields = set(required_fields + optional_fields + ['action'])

        # Verifica se todos os campos obrigatórios estão presentes
        missing_fields = [field for field in required_fields if field not in value]
        if missing_fields:
            self._errors.append(f"Campos obrigatórios ausentes para a ação '{action}': {', '.join(missing_fields)}.")
            return False

        # Verifica se há campos inesperados
        unexpected_fields = [field for field in value if field not in allowed_fields]
        if unexpected_fields:
            self._errors.append(f"Campos inesperados para a ação '{action}': {', '.join(unexpected_fields)}.")
            return False

        return True

    def fail(self, value):
        return " ".join(self._errors)


def config_validator(base_dir: str) -> bool:
    """
    Valida um arquivo YAML contra um esquema definido.

    Args:
        base_dir (str): Base dir.

    Returns:
        bool: True se o arquivo for válido, False caso contrário.
    """
    config_path = os.path.join(base_dir, '.config.yml')
    utis_base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(utis_base_dir, 'schema.yml')

    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # print(content)
    data = yamale.make_data(content=content)
    validators = DefaultValidators.copy()
    validators[StepValidator.tag] = StepValidator
    schema = yamale.make_schema(schema_path, validators=validators)    
    # print(f"Schema: {schema}")
    try:
        yamale.validate(schema, data)
        # print("Schema is valid.")
        return True
    except yamale.YamaleError as exc:
        print(".config.yml isn't valid.")
        print(exc)
        return False


def convert_windows_path_to_posix_path(path: str) -> str:
    """
        Converts a Windows file path to a POSIX-compliant path.

        Args:
            path (str): The file path to be converted.

        Returns:
            str: The converted file path.
        """
    try:
        path_converted = Path(path).as_posix()
        if path != path_converted:
            print(f"Converting path: {path} to {path_converted}")
        return path_converted
    except KeyError as exc:  #Verificar: esta é a mensagem de erro correta?
        print(f"Erro ao converter os paths dos repositorios: {exc}")
        raise


def check_config_name():
    config_files = ['config.yml', 'config.yaml']
    config_file = None
    
    for file in config_files:
        if os.path.exists(os.path.join(os.getcwd(), file)):
            config_file = file
            break

    if config_file is None:
        raise FileNotFoundError("Config file not founded (.config.yml ou .config.yaml).")

    return config_file


def load_config():
    """
        Load the configuration from the YAML file.

        Returns:
            dict: The loaded configuration.
    """
    #print("Getting config file...")
    
    config_path = os.path.join(os.getcwd(), "config.yml")

    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            #print(f"Load configuration with success!")
            return config
        except FileNotFoundError:
            print(f"Aviso: arquivo config.yml não encontrado em: {os.getcwd()}. Usando configurações padrão (se houver).")
            return {}
        except yaml.YAMLError as e:
            print(f"Erro ao ler o arquivo config.yml: {e}")
            return {}


def get_task(task_name: str) -> dict:
    """
    Load the configuration from the YAML file and return the task details.
    
    Args:
        task_name (str): The name of the task to retrieve.
    
    Returns:
        dict: The task details.
    """
    #print("Getting task parameters...")
    try:
        config = load_config()
        task = config["tasks"].get(task_name)
        if task != None:
            return task
        else:
            raise KeyError(f"Task '{task_name}' not founded.")
    except KeyError as exc:  #Verificar: esta é a mensagem de erro correta?
        print(f"Error getting desired task: {exc}")
        raise


def convert_paths_in_config_file():
    """
        Converts all Windows paths in the configuration file to POSIX-compliant paths.
    """
    config = load_config()
    base_path = config.get('base_path')
    if base_path:
        config['base_path'] = convert_windows_path_to_posix_path(base_path)

    tasks = config.get('tasks', {})
    for task_name, task_details in tasks.items():
        task_details['repository'] = convert_windows_path_to_posix_path(task_details['repository'])
    
    config_file = check_config_name()
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
