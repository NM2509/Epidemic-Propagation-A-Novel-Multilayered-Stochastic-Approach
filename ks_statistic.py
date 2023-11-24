np.random.seed(42)
random.seed(42) 

cluster_sizes_at_isolation = []

Traceable_probability = 0.06

while len(cluster_sizes_at_isolation) < 100:
    c = run_simulation()[3]
    for element in c:
        cluster_sizes_at_isolation.append(element)

clusters = pd.DataFrame(cluster_sizes_at_isolation, columns = ['size'])
data = clusters['size']

# Calculate parameter
geom_p = 1 / np.mean(data)

# KS test
ks_stat_geom, p_val_geom = kstest(data, 'geom', args=(geom_p,))
print("Kolmogorov-Smirnov Statistic:", ks_stat_geom.round(2), "P-value:", p_val_geom)
