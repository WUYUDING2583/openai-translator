from model import Model
import simplejson
import requests


class GLMModel(Model):
    def __init__(self, model_url: str, timeout: int):
        self.model_url = model_url
        self.timeout = timeout

    def make_request(self, prompt):
        try:
            payload = {"prompt": prompt, "history": []}
            response = requests.post(self.model_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            response_dict = response.json()
            translation = response_dict["response"]
            return translation, True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Exception: {e}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"Request Timeout: {e}")
        except simplejson.errors.JSONDecodeError as e:
            raise Exception("Error: response is not valid JSON format.")
        except Exception as e:
            raise Exception(f"Unkown error: {e}")

        return "", False
