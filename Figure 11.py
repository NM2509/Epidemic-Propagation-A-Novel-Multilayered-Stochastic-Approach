######################################################
# Figure 11: Distribution of simulated cluster sizes #
######################################################

np.random.seed(10)
random.seed(10) 

# Default parameters
Global_rate = 0.1 
Recovery_rate = 0.15 
Local_rate = 0.5
Confirmation_rate = 0.05
traceable_probability = [0.06, 0.2, 0.4, 0.6, 0.8, 0.9]

plt.figure(figsize = (20,10))

for i in range(6):
    plt.subplot(2, 3, i+1)
    
    cluster_sizes_at_isolation = []
    Traceable_probability = traceable_probability[i]
        
    while len(cluster_sizes_at_isolation) < 1000:
        c = run_simulation()[3]
        for element in c:
            cluster_sizes_at_isolation.append(element)
        
    clusters = pd.DataFrame(cluster_sizes_at_isolation, columns = ['size'])
    
    # Calculate the sample mean
    mean = np.mean(clusters['size'])
    
    # Estimating parameter p 
    p = 1 / mean
    
    # Geometric distribution with pre-specified parameter
    x = np.arange(1, max(clusters['size'])+1)
    y = geom.pmf(x, p)

    # Plot
    sns.histplot(data=clusters, 
                 x = 'size', 
                 bins = range(int(clusters['size'].min()), int(clusters['size'].max()) + 2), 
                 discrete = True, 
                 color = 'skyblue',
                 stat = 'probability')
    plt.scatter(x, y, color='red', label=f'Fitted Geometric Distribution, \nwith parameter p = {round(p,2)}')
    plt.plot(x, y, 'r-', lw=1)
    plt.xticks(range(int(clusters['size'].min()), int(clusters['size'].max()) + 1), size = 16)
    plt.xlabel('Cluster size', size = 16)
    plt.ylabel('Frequency', size = 16)
    plt.title('Traceable_probability: {}'.format(Traceable_probability), size = 18)
    plt.legend(prop={'size': 16})
    
plt.subplots_adjust(left=0.05, right=0.95, wspace=0.3, hspace = 0.3) 
plt.savefig('cluster_sizes.png', dpi = 300)
plt.show()
