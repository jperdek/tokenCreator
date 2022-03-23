from token_derivation.nodejs.construct_controller import ControllerConstructor


class ControllerInfo:
    def __init__(self, controller_name: str, controller_file_name: str, original_path: str):
        self.controller_name = controller_name
        self.original_path = original_path
        self.controller_file_name = controller_file_name

    def get_controller_name(self) -> str:
        return self.controller_name

    def get_controller_file_name(self) -> str:
        return self.controller_file_name

    def add_controller_to_instance(self, path_to_generated_server: str):
        specific_services = [
            ControllerConstructor.get_html_file_support(self.original_path, path_to_generated_server)
        ]
        controller_construction = ControllerConstructor.construct_controller(specific_services)
        ControllerConstructor.write_controller_to_file(
            path_to_generated_server, self.controller_file_name, controller_construction)
