def list_splitter(list, pieces):
    x = len(list)/pieces
    if len(list)%float(pieces) != 0:
        x += 1
    last = 0
    while last < len(list):
        start = last
        end = last + x
        if end > len(list):
            end = len(list)
        last = end
        yield list[start:end]
