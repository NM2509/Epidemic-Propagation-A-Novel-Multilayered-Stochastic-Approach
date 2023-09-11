###############################################################
# Getting connected cluster to isolate: below three functions #
###############################################################

# 1. Going up to the earliest node we have connection to, 
# and from there we will use get_connected_children 
# to get connected cluster

def get_earliest_parent_node(confirmed_node):
    earliest_node_reached = False
    current_node = confirmed_node
    while earliest_node_reached != True:
        if current_node.traceable == True:
            up_node = current_node.parent
            if up_node.active == True:
                current_node = up_node
            elif up_node.active == False:
                current_node = current_node
                earliest_node_reached = True
        elif current_node.traceable == False:
            earliest_node_reached = True
    return current_node

# 2. Getting sub-tree with a root vertex as the 'earliest_node'

def get_connected_children(earliest_node):
    nodes_to_isolate = []
    # Get all children
    traceable_children = earliest_node.traceable_children
    for child in traceable_children:
            if child.active == True:
                nodes_to_isolate.extend([child])       
    # Get children of children, etc via loop
    next_children_layer = []
    all_traceable_children_isolated = False
    while all_traceable_children_isolated != True:
        # Get all children of children which are traceable
        for node in traceable_children:
            next_children_layer.extend(node.traceable_children)
        # Only keep active children
        next_children_layer = [child for child in next_children_layer 
                               if child.active == True]
        if next_children_layer == []:
            all_traceable_children_isolated = True
        else:
            nodes_to_isolate.extend(next_children_layer)
            traceable_children = next_children_layer
            next_children_layer = []
            
    return nodes_to_isolate

# Note that we only consider links between active nodes. 
# Once a node becomes inactive, its links become irrelevant

# 3. Connecting previous two functions together

def get_connected_cluster(confirmed_node):
    nodes_to_isolate = []
    # Get the earliest node from which to branch out
    earliest_node = get_earliest_parent_node(confirmed_node)
    nodes_to_isolate.extend([earliest_node])
    # Get all children from the earliest node
    children_to_isolate = get_connected_children(earliest_node)
    nodes_to_isolate.extend(children_to_isolate)
    
    return nodes_to_isolate
