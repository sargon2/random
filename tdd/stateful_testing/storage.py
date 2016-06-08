import pickle

in_memory_item = None

def get_from_memory():
    return in_memory_item

def store_in_memory(item):
    global in_memory_item
    in_memory_item = item


data = {}
def store(key, item):
    global data
    data[key] = item
    pickle.dump(data, open("/tmp/state.p", "wb"))

def get(key):
    global data
    data = pickle.load(open("/tmp/state.p", "rb"))
    return data[key]
