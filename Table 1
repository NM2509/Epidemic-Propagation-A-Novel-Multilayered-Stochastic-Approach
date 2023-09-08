#############################################################
# Table 1: Cluster statistics with default parameter values #
#############################################################

np.random.seed(10)
random.seed(10)

# Default parameters
Global_rate = 0.1
Recovery_rate = 0.15 
Local_rate = 0.5
Confirmation_rate = 0.05 
Traceable_probability = 0.06


clusters = []

for i in range(1, 201):
    clusters_data = run_simulation(True)[6]
    clusters.append(clusters_data)
clusters_flat = [cluster for sublist in clusters for cluster in sublist]
print('Overall number of clusters:', len(clusters_flat))

# Average number of children per cluster
number_of_child_clusters = []

for cluster in clusters_flat:
    number_of_child_clusters.append(len(cluster.child_clusters))

average = np.array(number_of_child_clusters).mean().round(3)

print('Average number of child clusters: ', average)

# Average size of cluster
size_of_clusters = []

for cluster in clusters_flat:
    size_of_clusters.append(cluster.size)

average = np.array(size_of_clusters).mean().round(3)

print('Average size of a cluster: ', average)
