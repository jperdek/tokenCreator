import json
from honey_token_generator.honey_token_constructor import create_honeypots


def load_from_json(path_to_json: str):
    with open(path_to_json, "r", encoding="utf-8") as file:
        return json.loads(file.read())


def perform_strategy_with_similar_files() -> None:
    honeypots_config = load_from_json("./generated_honeypots.json")
    for strategy in honeypots_config:
        create_honeypots(honey_token_data=strategy["honey_token_data"],
                         path_to_server=strategy["path_to_server"],
                         path_to_server_stub=strategy["path_to_server_stub"])


def perform_strategy_with_deep_customization() -> None:
    honeypots_config = load_from_json("./generated_honeypots_customizable.json")
    for strategy in honeypots_config:
        create_honeypots(honey_token_data=strategy["honey_token_data"],
                         path_to_server=strategy["path_to_server"],
                         path_to_server_stub=strategy["path_to_server_stub"])


if __name__ == "__main__":
    # perform_strategy_with_similar_files()
    perform_strategy_with_deep_customization()
