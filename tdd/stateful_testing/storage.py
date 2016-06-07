import pickle

in_memory_item = None

def get_from_memory():
    return in_memory_item

def store_in_memory(item):
    global in_memory_item
    in_memory_item = item


def store(item):
    pickle.dump(item, open("/tmp/state.p", "wb"))

def get():
    return pickle.load(open("/tmp/state.p", "rb"))
