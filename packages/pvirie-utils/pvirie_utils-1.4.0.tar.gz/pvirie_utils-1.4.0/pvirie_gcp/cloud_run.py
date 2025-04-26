from pydantic import BaseModel
from enum import Enum
from typing import List, Dict, Any
import json
import getpass
import copy

from . import gcp, secret_manager

class Environment_Variable_Type(str, Enum):
    GCP_Secret = "gcp_secret"
    Static = "static"
    Container_Address = "container-address"
    Service_Address = "service-address"


class Environment_Variable(BaseModel):
    name: str
    variable: str
    type: Environment_Variable_Type
    secret: Dict[str, Any]

    def prompt(self, containers, parent_change=None, prefix=""):
        self_dict = self.model_dump()
        if self.type == Environment_Variable_Type.GCP_Secret:
            if parent_change is None or parent_change is True:
                r = input(f"{prefix}Do you want to upload new secret {self.name} to GCP? (y/N): ")
                if r.lower().strip() == "y":
                    secret_value = getpass.getpass(f"{prefix}Enter the value of the secret {self.name}: ")
                    self_dict["new_value"] = secret_value
        elif self.type == Environment_Variable_Type.Container_Address:
            # use localhost:port for address
            container_name = self.secret["name"]
            matched_container = next((c for c in containers if c.name == container_name), None)
            if matched_container:
                self_dict["resolved_address"] = f"localhost:{matched_container.port}"
            else:
                raise ValueError(f"{prefix}Container {container_name} not found in the deployment plan.")

        return self_dict


class Container(BaseModel):
    name: str
    image_url: str
    region: str = None
    port: int = None
    command: List[str] = None
    depends: List[str] = None
    env: List[str] = None

    def prompt(self, containers, envs: List[Environment_Variable] = None, parent_change=None, prefix=""):
        # Use latest or specific version?
        default_change = False
        if parent_change is None or parent_change is True:
            r = input(f"{prefix}Do you want to customize the container {self.name} parameters? (y/N): ")
            if r.lower().strip() == "y":
                default_change = True

        env_data = []
        for env_name in self.env:
            matched_env = next((env for env in envs if env.name == env_name), None)
            if matched_env:
                env_data.append(matched_env.prompt(containers, parent_change=default_change, prefix=prefix + "\t"))
            else:
                raise ValueError(f"{prefix}Environment variable {env_name} not found in the deployment plan.")
        
        self_dict = self.model_dump()
        # override the env with the new data
        self_dict["env"] = env_data
        return self_dict
    

class Service(BaseModel):
    name: str
    containers: List[Container]

    def prompt(self, envs: List[Environment_Variable] = None, parent_change=None, prefix=""):
        # Any parameter change? if so go deep down
        default_change = False
        if parent_change is None or parent_change is True:
            r = input(f"{prefix}Do you want to customize the service {self.name} parameters? (y/N): ")
            if r.lower().strip() == "y":
                default_change = True

        container_data = [c.prompt(self.containers, envs, parent_change=default_change, prefix=prefix + "\t") for c in self.containers]
        self_dict = self.model_dump()
        # override the containers with the new data
        self_dict["containers"] = container_data
        return self_dict


class Deploy_Plan(BaseModel):
    variables: List[Environment_Variable]
    services: List[Service]

    def provision(self) -> "Deploy_Executor":
        """
        Provision the deployment plan.
        """
        default_change = False
        r = input(f"Do you want to customize the plan? (y/N): ")
        if r.lower().strip() == "y":
            default_change = True
        service_data = [s.prompt(self.variables, parent_change=default_change) for s in self.services]
        return Deploy_Executor(service_data)
    

    @staticmethod
    def from_json_file(file_path: str) -> "Deploy_Plan":
        """
        Load a deployment plan from a file.
        """
        with open(file_path, "r") as file:
            data = json.load(file)
            return Deploy_Plan(**data)
        

    @staticmethod
    def from_json_string(json_string: str) -> "Deploy_Plan":
        """
        Load a deployment plan from a JSON string.
        """
        data = json.loads(json_string)
        return Deploy_Plan(**data)
    


class Deploy_Executor:
    def __init__(self, plan_data: List[Dict[str, Any]]):
        self.plan_data = plan_data

    def __str__(self):
        clone_data = copy.deepcopy(self.plan_data)
        # censure sensitive data, e.g. secrets
        for service in clone_data:
            for container in service["containers"]:
                for env in container["env"]:
                    if env["type"] == Environment_Variable_Type.GCP_Secret and "new_value" in env:
                        env["new_value"] = "********"
        json_str = json.dumps(clone_data, indent=4)
        return json_str

    def __call__(self):
        """
        Execute the deployment plan.
        """
        credentials = gcp.get_credentials()
        gcp.ensure_console_login()
        sm = secret_manager.Secret_Manager(credentials=credentials)
