import json

import apiai

TOKEN = '77eace71019e4092adfe1bcd32d93a47'

class Chatbot:
    def __init__(self):
        self.ai = apiai.ApiAI(TOKEN)

    def clean(self, data):
        pass
    def speak(self, query):
        self.request = self.ai.text_request()
        self.request.session_id = 'generic'
        self.request.query = query
        # return self.request.getresponse().read().get('result')['fulfillment']['speech']
        data = json.loads(
            self.request.getresponse().read().decode('utf-8')
        )

        return data.get('result')['fulfillment']['messages'][0]['speech']
