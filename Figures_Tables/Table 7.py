###########
# Table 7 #
###########

np.random.seed(10)
random.seed(10) 

Global_rate = 0.12
Recovery_rate = 0.20
Local_rate = 0.47
sizes = [1,2,3,4,5,6,7,8,9]
probs = [0.235, 0.290, 0.182, 0.194, 0.064, 0.025, 0.006, 0.003, 0.001]

# Parameters to vary
Traceable_probabilities = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
Confirmation_rates = [0, 0.01, 0.05, 0.075]

# Creating plots
proportions = []

# Print out simulations number
sim = 0

for m in range(len(Confirmation_rates)):
    for g in range(len(Traceable_probabilities)):
        
        sim += 1
    
        # Set rates
        Confirmation_rate = Confirmation_rates[m]
        Traceable_probability = Traceable_probabilities[g]
        
        # To record probability of survival
        k = 0

        for i in range(1, 100):
            results = run_simulation()
            # for calculating proportion of survival cases after 1 year
            active_nodes = results[1]
            if len(active_nodes) == 0:
                outcome = 0
            elif len(active_nodes) > 0:
                outcome = 1
            k += outcome
            
        proportions.append(((Confirmation_rate, Traceable_probability), k/100))
        print('Simulation: {}'.format(sim))
        print(((Confirmation_rate, Traceable_probability), k/100))

data = proportions.copy()

# Creating DataFrame
df = pd.DataFrame()
for coord, value in data:
    row, col = coord
    df.at[row, col] = value
df = 1 - df

# Hetamap
plt.figure(figsize=(7, 5))
sns.heatmap(df, cmap = 'Blues', annot = True, fmt=".2f")
plt.title('Probability of extinction within one year', fontsize = 16)
plt.xlabel('Traceable probability', fontsize = 16)
plt.ylabel('Confirmation rate', fontsize = 16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.subplots_adjust(left=0.1, right=0.95, wspace=0.3) 
plt.savefig('confirmation_testing.png', dpi = 300)
plt.show()
