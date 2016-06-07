import pickle

class StatefulBoolean(object):
    def set_state(self, state):
        # TODO: test on Windows when the /tmp/ folder doesn't exist
        pickle.dump(state, open("/tmp/state.p", "wb"))

    def get_state(self):
        return pickle.load(open("/tmp/state.p", "rb"))
