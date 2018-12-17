

def label_sort(data, entries_pp):
    # Grab the total number of lines
    line_count = 0
    for line in data:
        line = line.decode().strip()
        if line.startswith("parent"):
            continue
        else:
            line_count += 1
