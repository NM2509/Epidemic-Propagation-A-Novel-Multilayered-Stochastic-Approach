###############
# Parameters: #
###############

# 1. Household sizes

def solve_weights_size_biased(sizes, probs):
    x = Symbol('x')
    equation = sum([s*p*x for s, p in zip(sizes, probs)]) - 1
    solution = solve(equation)
    weighted_probabilities = [s*p*solution[0] for 
                              s, p in zip(sizes, probs)]
    return weighted_probabilities

def create_size_biased_distribution_100000_values(sizes, probs): 
    weighted_probabilities = solve_weights_size_biased(sizes, probs)
    distribution = np.random.choice(sizes, 
                                    p = weighted_probabilities, 
                                    size = 100000)
    return distribution


# 2. SIR dynamic inside household

def birth_rate_function(i): 
    rate = i * Global_rate
    return rate

def infection_rate_function(susceptible, infected, household_size):
    if (susceptible == 0) or (household_size == 1):
        rate = 0
    else:
        rate = Local_rate * infected * (susceptible / (household_size - 1))
    return rate

def recovery_rate_function(infected):
    rate = Recovery_rate * infected
    return rate

def confirmation_rate_function(infected):
    rate = Confirmation_rate * infected
    return rate

# 3. Traceability

def edge_status(household_id):
    if household_id == '0':
        edge_status = False
    else:
        traceability = [True, False]
        probabilities = [Traceable_probability, 1 - Traceable_probability]
        edge_status = random.choices(traceability, probabilities)[0]
    return edge_status

############################
# Default parameter values #
############################

sizes = [1,2,3,4,5] 
probs = [0.2, 0.2, 0.2, 0.2, 0.2]
Global_rate = 0.1
Recovery_rate = 0.15 
Local_rate = 0.5 
Confirmation_rate = 0.05
Traceable_probability = 0.06
