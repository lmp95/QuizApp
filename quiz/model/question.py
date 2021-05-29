import json


class Question:
    def __init__(self, id, moduleId, question, choices, answer):
        self.id = id
        self.moduleId = moduleId
        self.question = question
        self.choices = choices
        self.answer = answer

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)