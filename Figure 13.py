#############
# Figure 13 #
#############

np.random.seed(10)
random.seed(10) 

# Parameters - London

Global_rate = 0.12
Recovery_rate = 0.20
Local_rate = 0.47
sizes = [1,2,3,4,5,6,7,8,9]
probs = [0.235, 0.290, 0.182, 0.194, 0.064, 0.025, 0.006, 0.003, 0.001]
size_biased_weights = solve_weights_size_biased(sizes, probs)

Traceable_probabilities = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
Confirmation_rates = [0.01, 0.05, 0.075, 0.1, 0.15, 0.2]

BRN_results = []

for l in range(len(Traceable_probabilities)):
    for j in range(len(Confirmation_rates)):
        
        integrals = []
        Basic_Reproduction_Numbers = []
        Traceable_probability = Traceable_probabilities[l]
        Confirmation_rate = Confirmation_rates[j]
        print('Detection: ', Confirmation_rate)
        print('Traceability (prob.): ', Traceable_probability)
        
        Basic_Reproduction_Numbers = R_0_estimation(Global_rate, 
                                                    Recovery_rate, 
                                                    Local_rate, 
                                                    Confirmation_rate, 
                                                    Traceable_probability, 
                                                    size_biased_weights, 
                                                    sizes)

        average = np.array(Basic_Reproduction_Numbers).mean().round(3)
        print('Average: ', average, '\n\n')
        BRN_results.append(average)

array = np.meshgrid(Confirmation_rates, Traceable_probabilities)
df = pd.DataFrame({
    'Traceable_probabilities': array[1].flatten(),
    'Confirmation_rates': array[0].flatten()
})
df['Average_BRN'] = BRN_results
heatmap_df = df.pivot('Traceable_probabilities', 'Confirmation_rates', 'Average_BRN')

# Hetamap
plt.figure(figsize=(7, 5))
sns.heatmap(heatmap_df, cmap = 'Blues', annot = True, fmt=".1f")
plt.title('Average Basic Reproduction Number, \nper varying detection and traceability efforts strengths\n', fontsize = 18)
plt.xlabel('Detection rate', fontsize = 16)
plt.ylabel('Traceable probability', fontsize = 16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.subplots_adjust(left=0.1, right=0.99, wspace=0.05, top = 0.80) 
plt.savefig('detection_and_tracing_2.png', dpi = 300)
plt.show()
