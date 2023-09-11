#############################################################################
# Function for choosing an event (birth, infection, recovery, confirmation) #
#############################################################################

events = ['birth','infection','recovery', 'confirmation']

def choose_event(total_rate, 
                 total_birth_rate, 
                 total_infection_rate, 
                 total_recovery_rate, 
                 total_confirmation_rate):

    # Event probabilities
    birth_probability = total_birth_rate/total_rate
    infection_probability = total_infection_rate/total_rate
    recovery_probability = total_recovery_rate/total_rate
    confirmation_probability = total_confirmation_rate/total_rate

    # Choose event (birth, infection, recovery, confirmation)
    probabilities = np.array([birth_probability, 
                              infection_probability, 
                              recovery_probability, 
                              confirmation_probability])
    
    # compute the cumulative sum of the probabilities
    cumulative_probabilities = np.cumsum(probabilities)

    # generate a random number
    random_number = np.random.rand()

    # find where this number would be inserted in the cumulative sum array
    index = np.searchsorted(cumulative_probabilities, random_number)
    
    chosen_event = events[index]
    
    return chosen_event
