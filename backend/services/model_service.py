from models.t5_model import T5Model


t5_model = T5Model()
t5_model.load_model()


def generate_answer(prompt):

    return t5_model.generate_response(prompt)


def train_model():

    return t5_model.train_model()