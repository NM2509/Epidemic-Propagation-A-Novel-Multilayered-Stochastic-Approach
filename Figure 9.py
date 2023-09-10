#####################################################################################################################
# Figure 9: BRN estimation - Estimation of the BRN for varying detection rate and traceable probability parameters #
#####################################################################################################################

# Parameters
sizes = [1,2,3,4,5] 
probs = [0.2, 0.2, 0.2, 0.2, 0.2]
probabilities = solve_weights_size_biased(sizes, probs)
size_biased_weights = solve_weights_size_biased(sizes, probs)

Local_rate = 1.0
Global_rate = 0.5
Recovery_rate = 0.15
Traceable_probability_list = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
Confirmation_rate_list = [0.01, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6]

BRN_results = []

np.random.seed(10)
random.seed(10) 

for l in range(len(Traceable_probability_list)):
    for j in range(len(Confirmation_rate_list)):
        
        integrals = []
        Basic_Reproduction_Numbers = []
        Traceable_probability = Traceable_probability_list[l]
        Confirmation_rate = Confirmation_rate_list[j]
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

# DataFrame
array = np.meshgrid(Confirmation_rate_list, Traceable_probability_list)
df_2 = pd.DataFrame({
    'Confirmation_rate_list': array[1].flatten(),
    'Traceable_probability_list': array[0].flatten()
})

df_2['Average_BRN'] = BRN_results
heatmap_df_2 = df_2.pivot('Confirmation_rate_list','Traceable_probability_list', 'Average_BRN')

# Hetamap
plt.figure(figsize=(10, 7))
sns.heatmap(heatmap_df_2.transpose(), cmap='Blues', annot=True, fmt=".1f")
plt.title('Average Basic Reproduction Number, \nper varying detection and traceability efforts strengths\n', fontsize=18)
plt.xlabel('Traceable probability', fontsize=16)
plt.ylabel('Detection rate', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.subplots_adjust(left=0.1, right=0.99, wspace=0.05, top=0.80) 
plt.savefig('detection_and_tracing_3.png', dpi=300)
plt.show()
