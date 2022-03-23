from token_derivation.nodejs.controller_info import ControllerInfo


class NodeJsBaseServer:
    def get_cors_handling_code(self, origin_domain = "*") -> str:
        return """
        app.use(function(req, res, next) {
          res.header("Access-Control-Allow-Origin", """ + origin_domain + """");
          res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
          res.header("Access-Control-Allow-Methods","GET,PUT,POST,DELETE");
          res.header("Host","http://localhost:5001");
          next();
        });
        """

    def base_server_stub(self, controllers: list['ControllerInfo'], path_to_server: str, add_cors=True) -> list['str']:
        server_stub_code = [
            "var express = require('express');",
            "var app = express();"
        ]
        if add_cors:
            server_stub_code.append("var cors = require('cors');")

        server_stub_code.append("var bodyParser = require('body-parser');")
        server_stub_code.append("const zlib = require('zlib');")

        for index, controller_to_insert in enumerate(controllers):
            controller_name = controller_to_insert.get_controller_name()
            controller_file_name = controller_to_insert.get_controller_file_name()
            server_stub_code.append(
                """var """ + controller_name + """ = require('./controllers/""" + controller_file_name + """');""")

            if index == 0:
                server_stub_code.append("const { createProxyMiddleware } = require('http-proxy-middleware');")
                server_stub_code.append("app.engine('html', require('ejs').renderFile);")
                server_stub_code.append("app.set('view engine', 'html');")

                server_stub_code.append("app.use(cors());")
                server_stub_code.append("app.use(bodyParser.json());")

            server_stub_code.append("""app.use('/', """ + controller_name + """);""")
            if index == 0:
                server_stub_code.append("app.use(express.static(__dirname + '/public/'));")

            controller_to_insert.add_controller_to_instance(path_to_server)

        if add_cors:
            server_stub_code.append(self.get_cors_handling_code())
        server_stub_code.append("app.listen(5001);")
        server_stub_code.append("")
        server_stub_code.append("console.log('Server up and running on port 5001');")
        return server_stub_code

    @staticmethod
    def write_to_file(path: str, server_stub_code: list['str']):
        with open(path, "w", encoding="utf-8") as file:
            file.writelines("\n".join(server_stub_code))


def construct_whole_server(path_to_server: str, controllers: list['ControllerInfo']):
    node_js_base_server = NodeJsBaseServer()
    base_server_stub = node_js_base_server.base_server_stub(controllers, path_to_server, add_cors=True)
    node_js_base_server.write_to_file(path_to_server + "/server.js", base_server_stub)


if __name__ == "__main__":
    controllers_to_insert = [
        ControllerInfo("business_domain", "business.domain", "./example/battle-chess.html")
    ]
    construct_whole_server("./generated", controllers_to_insert)
