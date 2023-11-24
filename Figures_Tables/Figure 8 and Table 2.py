#####################################################################################################################
# Figure 8 and Table 2: Simulations of the number of active nodes through time for different levels of global infection rate, β #
#####################################################################################################################

np.random.seed(10)
random.seed(10)

# Default parameters
Recovery_rate = 0.15 
Confirmation_rate = 0.05
Traceable_probability = 0.06

# Infection rate parameters
Local_rate = 0.3
global_beta = [0.05, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]

# Plots
sns.set_style("darkgrid")
proportions = []
list_of_results = []

plt.figure(figsize=(14, 16))

for i in range(8):
    Global_rate = global_beta[i]
    list_of_results.append('beta = {}'.format(Global_rate))
    
    plt.subplot(4,2,i+1)
    
    times_of_extinction = []

    k = 0
    
    for i in range(1, 100):
        results = run_simulation(False)
        
        # for calculating proportion of survival cases after 1 year
        active_nodes = results[1]
        if len(active_nodes) == 0:
            outcome = 0
        elif len(active_nodes) > 0:
            outcome = 1
        k += outcome
        
        # for plots
        data = results[2]
        times_of_extinction.append(data['Time'].max())
        plt.plot(data['Time'], data['Active nodes'])
            
    proportions.append((Global_rate, k/100))    
    # add title and labels
    plt.title('Global rate = {}'.format(Global_rate), fontsize=16)
    plt.xlabel('Time, in Days\n\n', fontsize=14)
    plt.ylabel('Number of Active Households', fontsize=14)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid(True)

plt.subplots_adjust(left=0.15, right=0.95, wspace=0.3, hspace = 1) 
plt.savefig('active_nodes_simulations.png', dpi = 300)
plt.show()

# Print the number of survival cases
proportions
