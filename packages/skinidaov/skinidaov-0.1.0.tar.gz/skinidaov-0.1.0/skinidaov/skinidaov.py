def to_base(id):
    id = str(int(id) + 1)
    id = f"{id[:3]}{id[-1]}" if id[3] == "0" else id
    return id

def to_standard(id):
    id = str(int(id) - 1)
    id = f"{id[:3]}0{id[-1]}" if len(id) == 4 else id
    return id