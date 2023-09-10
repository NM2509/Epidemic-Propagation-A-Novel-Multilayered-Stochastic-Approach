###################################################################
# Table 3: BRN estimation - default case - discrete approximation #
###################################################################

np.random.seed(10)
random.seed(10)

# Default parameters
sizes = [1,2,3,4,5] 
probs = [0.2, 0.2, 0.2, 0.2, 0.2]
Global_rate = 0.1
Recovery_rate = 0.15 
Local_rate = 0.5 
Confirmation_rate = 0.05
Traceable_probability = 0.06
size_biased_weights = solve_weights_size_biased(sizes, probs)

Basic_Reproduction_Numbers = R_0_estimation(Global_rate, 
                   Recovery_rate, 
                   Local_rate, 
                   Confirmation_rate, 
                   Traceable_probability, 
                   size_biased_weights,
                   sizes)

mean = np.array(Basic_Reproduction_Numbers).mean()
std = np.sqrt(np.array(Basic_Reproduction_Numbers).var())
minimum = np.array(Basic_Reproduction_Numbers).min()
maximum = np.array(Basic_Reproduction_Numbers).max()
print('Average BRN: ', mean.round(3))
print('Standard deviation: ', std.round(3))
print('Minimum: ', minimum.round(3))
print('Maximum: ', maximum.round(3))
