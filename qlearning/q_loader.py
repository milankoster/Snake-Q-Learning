import pickle


def load_q_table(episode):
    filename = f"../models/qlearning/{episode}.pickle"
    with open(filename, 'rb') as file:
        q_table = pickle.load(file)
        return q_table
