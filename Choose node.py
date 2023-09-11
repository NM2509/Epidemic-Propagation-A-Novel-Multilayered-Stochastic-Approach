###################################################################
# Function for choosing a node (through index in a list of nodes) #
###################################################################

def choose_index_of_node(probabilities, 
                         random_numbers, 
                         iteration_index):
    
    # cumulative sum of the probabilities
    cumulative_probabilities = cumsum_numba(probabilities)
    
    # random number between 0 and 1
    random_number = random_numbers[iteration_index]
    
    # where this number is inserted in the cumulative sum array
    index = np.searchsorted(cumulative_probabilities, random_number)
    
    return index
