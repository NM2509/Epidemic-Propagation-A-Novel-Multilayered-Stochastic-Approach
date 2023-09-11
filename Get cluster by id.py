###################################
# Function: getting cluster by id #
###################################

def get_cluster_by_id(clusters, parent_id):
    matching_clusters = [cluster for cluster in clusters 
                         if cluster.cluster_id == parent_id]
    return matching_clusters[0] if matching_clusters else 'Error: check cluster data'
