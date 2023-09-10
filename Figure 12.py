#############
# Figure 12 #
#############

# Parameters - London

Global_rate = 0.12
Recovery_rate = 0.20
Local_rate = 0.47
Confirmation_rate = 0
Traceable_probability = 0

sizes = [1,2,3,4,5,6,7,8,9]
probs = [0.235, 0.290, 0.182, 0.194, 0.064, 0.025, 0.006, 0.003, 0.001]

np.random.seed(10)
random.seed(10) 

# Creating plots
sns.set_style("darkgrid")
proportions = []
list_of_results = []
proportions = []

plt.figure(figsize=(10, 5))

times_of_extinction = []

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

    # plots
    data = results[2]
    times_of_extinction.append(data['Time'].max())
    plt.plot(data['Time'], data['Active nodes'])

proportions.append((Global_rate, k/100))   

# Add title and labels
plt.title('Number Of Infected Households Through Time\n', fontsize=16)
plt.xlabel('Time, in Days\n\n', fontsize=14)
plt.ylabel('Number of Active Households', fontsize=14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.grid(True)
plt.subplots_adjust(left=0.15, right=0.95, wspace=0.3, hspace = 1) 
plt.savefig('nodes_with_no_intervention.png', dpi = 300)
plt.show()
