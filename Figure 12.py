############################
# Figure 12: semi-log plot #
############################

np.random.seed(10)
random.seed(10) 

# Default parameters
Global_rate = 0.1
Recovery_rate = 0.15
Local_rate = 0.5
Confirmation_rate = 0.05
Traceable_probability = 0.06

cluster_sizes_at_isolation = []

while len(cluster_sizes_at_isolation) < 1000:
    c = run_simulation()[3]
    for element in c:
        cluster_sizes_at_isolation.append(element)
clusters = pd.DataFrame(cluster_sizes_at_isolation, columns = ['size'])

# Semi-log plot
sns.set_style("darkgrid")
data = cluster_sizes_at_isolation
values, counts = np.unique(data, return_counts=True)
probabilities = counts / len(data)
log_probabilities = np.log(probabilities)

plt.figure(figsize=(10, 6))
plt.scatter(values, log_probabilities, color='blue', label='Data')
plt.title('Semi-Log Plot for Cluster Sizes at Isolation\n', size = 20)
plt.xlabel('Sizes', size = 18)
plt.ylabel('Log (Probabilities)', size = 18)
plt.xticks(size = 16)
plt.yticks(size = 16)
plt.grid(True, which="both", ls="--", c='0.7')
plt.savefig('semi_log_plot.png', dpi = 300)
plt.show()
