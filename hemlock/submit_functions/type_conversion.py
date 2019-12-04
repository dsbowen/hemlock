"""Type conversion on question submission"""

def resp_to_int(q):
    q.response = int(q.response)

def data_to_int(q):
    q.data = int(q.data)

def resp_to_float(q):
    q.response = float(q.response)

def data_to_float(q):
    q.data = float(q.data)