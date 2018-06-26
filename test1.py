routers = {}
with open('file.txt', 'r') as file:
    lines = file.read().splitlines()
    for i in lines:
        split_lines = i.split(' ')
        if split_lines[0] not in routers:
            routers[split_lines[0]] = []
            add_to_routers = routers[split_lines[0]].append(split_lines[1])
        else:
            add_to_routers = routers[split_lines[0]].append(split_lines[1])
    print routers
