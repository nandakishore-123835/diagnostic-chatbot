from models.t5_model import T5Model


t5_model = T5Model()


def generate_answer(prompt):

    return t5_model.generate_response(prompt)