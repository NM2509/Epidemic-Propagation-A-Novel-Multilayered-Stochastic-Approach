###############################################################################################################
# Table 4: BRN estimation - Varying Detection Rate - BRN statistics obtained from 100 clusters per simulation #
###############################################################################################################

np.random.seed(10)
random.seed(10)

# Default parameters
Global_rate = 0.1
Recovery_rate = 0.15 
Local_rate = 0.5 
Traceable_probability = 0.06
size_biased_weights = solve_weights_size_biased(sizes, probs)
sizes = [1,2,3,4,5]

# Varying detection rate
Confirmation_rate_list = [0, 0.1, 0.2, 0.5, 1]

BRN_results = []

for h in range(len(Confirmation_rate_list)):
    print('Confirmation rate: ', Confirmation_rate_list[h])
    Confirmation_rate = Confirmation_rate_list[h]
    
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
