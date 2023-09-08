####################################################################################
# Figure 7: Number of active households in 200 simulations with default parameters #
####################################################################################

np.random.seed(10)
random.seed(10)

sns.set_style('darkgrid')
plt.figure(figsize=(20, 6))

for i in range(2):
    plt.subplot(1,2,i+1)
    if i == 0:
        times_of_extinction = []

        for i in range(1, 201):
            data = run_simulation()[2]
            times_of_extinction.append(data['Time'].max())
            plt.plot(data['Time'], data['Active nodes'])

        plt.title('Number of Active Households Over Time per 200 Simulations', fontsize=19)
        plt.xlabel('Time, in Days', fontsize=16)
        plt.ylabel('Number of Active Households', fontsize=16)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.grid(True)
        
    if i == 1:
        sns.histplot(times_of_extinction)
        plt.xlabel('Time, in Days', fontsize = 16)
        plt.ylabel('Frequnecy', fontsize = 16)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.title('Distribution of Extinction times in 200 simulations', fontsize = 19)

plt.subplots_adjust(left=0.05, right=0.95, wspace=0.3) 
plt.savefig('number_of_active_nodes.png', dpi = 300)
plt.show()
