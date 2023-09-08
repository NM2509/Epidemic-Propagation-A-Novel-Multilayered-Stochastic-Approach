######################################################
# Table 5: Recovery: Comparison with Bertoin's paper #
######################################################

# Parameters
sizes = [1] 
probs = [1]
Local_rate = 0
Global_rate = 0.5
Confirmation_rate = 0.05
Traceable_probability = 0.06
Recovery_rate_list = [0, 0.1, 0.2, 0.5, 1]

# Simulations

np.random.seed(10)
random.seed(10)

size_biased_weights = solve_weights_size_biased(sizes, probs)

for h in range(len(Recovery_rate_list)):
    print('Recovery rate: ', Recovery_rate_list[h])
    Recovery_rate = Recovery_rate_list[h]
    
    Basic_Reproduction_Numbers = R_0_estimation(Global_rate, 
                   Recovery_rate, 
                   Local_rate, 
                   Confirmation_rate, 
                   Traceable_probability, 
                   size_biased_weights, 
                   sizes)

    print('Average: ', np.array(Basic_Reproduction_Numbers).mean().round(3))   
    print('Standard deviation: ', np.sqrt(np.array(Basic_Reproduction_Numbers).var()).round(3))
    print('Minimum: ', min(Basic_Reproduction_Numbers).round(3))
    print('Maximum: ', max(Basic_Reproduction_Numbers).round(3))
    print('\n')
