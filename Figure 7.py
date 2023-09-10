############################################################################################
# Figure 7: Varying local and global infection rates to analyse effect of transmissibility #
############################################################################################

np.random.seed(10)
random.seed(10)

# Default parameters
Recovery_rate = 0.15 
Confirmation_rate = 0.05 
Traceable_probability = 0.06

# Parameters to vary
local_lambda = [0.02, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 1]
global_beta = [0.05, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]

# Create DataFrame
array = np.meshgrid(local_lambda, global_beta)
df = pd.DataFrame({
    'local_lambda': array[0].flatten(),
    'global_beta': array[1].flatten()
})

child_clusters = []

# Iterating through each of the combination of global and local infection rates
for l in range(len(global_beta)):
    for j in range(len(local_lambda)):
        inactive_clusters = []
        Global_rate = global_beta[l]
        Local_rate = local_lambda[j]
        print('Local rate: ', Local_rate)
        print('Global rate: ', Global_rate)
        
        while len(inactive_clusters) < 200:
            results = run_simulation(True, max_population_BRN_simulation = 500000)
            # if the simulation ran for too long without obtaining any result
            if results == 'death_of_cluster_undetected':
                print('Death_of_cluster_undetected: possible bias')
                break
            else:
                clusters = results[6]
                # append inactive clusters
                inactive_clusters.append(clusters[0:2])
                
        if results == 'death_of_cluster_undetected':
            pass   
        
        # get clusters and their statistics
        else:
            clusters_flat = [cluster for sublist in inactive_clusters for cluster in sublist]
            clusters_flat = clusters_flat[0:200]

            number_of_child_clusters = []
            for cluster in clusters_flat:
                number_of_child_clusters.append(len(cluster.child_clusters))
            print('Number of clusters: ', len(clusters_flat))

            average = np.array(number_of_child_clusters).mean().round(10)
            print('Average: ', average, '\n\n')
            child_clusters.append(average)

df['average_children'] = child_clusters
heatmap_df = df.pivot('local_lambda', 'global_beta', 'average_children')

# Hetamap
plt.figure(figsize=(7, 5))
sns.heatmap(heatmap_df, cmap = 'Blues', annot = True, fmt=".2f")

plt.title('Average number of child clusters, per cluster\n per a combination of local and global infection rates\n', fontsize = 16)
plt.xlabel('Global infection rate', fontsize = 16)
plt.ylabel('Local infection rate', fontsize = 16)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.subplots_adjust(left=0.1, right=0.95, wspace=0.3, top = 0.85) 
plt.savefig('average_cluster_children_per_infection_rates.png', dpi = 300)
plt.show()
