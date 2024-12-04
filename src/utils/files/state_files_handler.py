import json
import os

from core.networks import Network


class JsonFilesHandler:
    @staticmethod
    def load_state(state_file: str) -> dict:
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_state(state_file: str, json_data: dict) -> None:
        with open(state_file, "w") as f:
            json.dump(json_data, f, indent=4)

class WebhookIdsHandler:
    def __init__(self, json_path):
        self.json_path = json_path

    def _get_json_key(self, network_abbr):
        return f'webhook_id_{network_abbr}'

    def get_webhook_id(self, network_abbr: str) -> str | None:
        """Get id of webhook by its network"""
        key = self._get_json_key(network_abbr)
        existing_json = JsonFilesHandler.load_state(self.json_path)
        if key in existing_json:
            return existing_json[key]
        return None
    
    def save_webhook_id(self, webhook_id: str, network_abbr: str) -> None:
        key = self._get_json_key(network_abbr)
        existing_json = JsonFilesHandler.load_state(self.json_path)
        existing_json[key] = webhook_id
        JsonFilesHandler.save_state(self.json_path, existing_json)

    def delete_webhook_id(self, network_abbr: str) -> None:
        key = self._get_json_key(network_abbr)
        existing_json = JsonFilesHandler.load_state(self.json_path)
        del existing_json[key]
        JsonFilesHandler.save_state(self.json_path, existing_json)

        

