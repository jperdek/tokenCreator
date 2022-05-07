class ControllerConstructor:
    @staticmethod
    def construct_controller(specific_services: list['str']) -> list['str']:
        controller_code = [
            "var express = require(\"express\")",
            "var moment = require(\"moment\")",
            "var router = express.Router();",
            "var fs = require('fs');",
            """router.use(
              express.urlencoded({
                extended: true
              })
            );""",
            "router.use(express.json());"
        ]
        for specific_service in specific_services:
            controller_code.append(specific_service)
        controller_code.append("module.exports = router")
        return controller_code

    @staticmethod
    def copy_file_to_server(path_to_html_file: str, html_file_name: str, path_to_server: str):
        with open(path_to_html_file, "r", encoding="utf-8") as read_file:
            with open(path_to_server + "/" + html_file_name, "w", encoding="utf-8") as write_file:
                write_file.write(read_file.read())

    @staticmethod
    def get_html_file_support(path_to_html_file: str, path_to_server: str) -> str:
        html_file_name = path_to_html_file[path_to_html_file.rfind("/") + 1:]
        ControllerConstructor.copy_file_to_server(path_to_html_file, html_file_name, path_to_server)
        return """
        router.get('/', function(req, res){
            fs.readFile('./""" + html_file_name + """',function(error, content){
                if(error){
                    res.writeHead(500);
                    res.end();
                } else {
                    res.writeHead(200, { 'Content-type': 'text/html' });
                    res.end(content, 'utf-8');
                }
            });
        });
        """

    @staticmethod
    def write_controller_to_file(path_to_server: str, controller_file_name: str, controller_code: list['str']):
        with open(path_to_server + "/controllers/" + controller_file_name + ".js", "w", encoding="utf-8") as file:
            file.writelines("\n".join(controller_code))

    @staticmethod
    def read_from_file(path: str):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def insert_detection_logic(path_to_detection_logic: str, listening_url: str, conceal_methods: str = None) -> str:
        detection_logic = ControllerConstructor.read_from_file(path_to_detection_logic)
        detection_logic = detection_logic.replace("/replaceMe", listening_url)
        if conceal_methods is not None:
            detection_logic = detection_logic.replace("<<[key]>>", conceal_methods)
        return detection_logic
