import requests
from app import app

def translate(text, source_language, dest_language):
    if "MS_TRANSLATOR_KEY" not in app.config or not app.config["MS_TRANSLATOR_KEY"]:
        return "Error: the translator service is not configured"
    auth = {
        "Ocp-Apim-Subscription-Key": app.config["MS_TRANSLATOR_KEY"],
        "Ocp-Apim-Subscription-Region": "eastus"
    }

    r = requests.post(f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={source_language}&to={dest_language}",
                      headers=auth, json=[{"Text": text}])
    if r.status_code != 200:
        return "Error: Translation failed"
    
    return r.json()[0]["translations"][0]["text"]
