#############################
# Clusters - defining class #
#############################

class Cluster():
    def __init__(self, origin, birth_time, parent_cluster):
        
        # Attributes - core
        self.households = [origin]
        self.origin = origin
        self.cluster_id = '0' if birth_time == 0 
                              else str(parent_cluster.cluster_id) +
                          "_" + str(len(parent_cluster.child_clusters))
        self.birth_time = birth_time
        
        # Attributes - parent and children
        self.parent = None
        self.child_clusters = []
        self.child_clusters_time = []
        
        # Attributes - initial conditions
        self.size = 1
        self.active = True
        
        # Attributes - times at which events occur to cluster
        self.infected_times = []
        self.recovered_times = []
        self.isolation_time = [] 
        
    # Method - household is added to cluster
    def add_household(self, household):
        self.households.append(household)
        self.size += 1
        return self

    # Method - returns all households that are part of a cluster
    def get_households(self):
        return self.households

    # Method - new child cluster is generated
    def create_new_cluster(self, new_origin, 
                           new_birth_time, parent_cluster):
        # Initialise new cluster
        new_cluster = Cluster(new_origin, new_birth_time, parent_cluster)
        # Attributes for parent and child clusters
        new_cluster.parent = self
        self.child_clusters.append(new_cluster)
        self.child_clusters_time.append(new_birth_time)
        return new_cluster
