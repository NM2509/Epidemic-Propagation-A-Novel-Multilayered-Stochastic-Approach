#######################
# Importing Libraries #
#######################

import numpy as np
import pandas as pd
import random
import warnings 
import cProfile
import matplotlib.pyplot as plt
import numba
from numba import jit 
import pstats
import seaborn as sns
from scipy.stats import geom
import time
from sympy.solvers import solve
from sympy import Symbol
from scipy.stats import kstest
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
    
#######################################
# Other functions used in simulations #
#######################################

# Function: getting cluster by id

def get_cluster_by_id(clusters, parent_id):
    matching_clusters = [cluster for cluster in clusters 
                         if cluster.cluster_id == parent_id]
    return matching_clusters[0] if matching_clusters else 'Error'


# Getting connected cluster to isolate: below three functions

# 1. Going up to the earliest node we have connection to, 
# and from there we will use get_connected_children 
# to get connected cluster

def get_earliest_parent_node(confirmed_node):
    earliest_node_reached = False
    current_node = confirmed_node
    while earliest_node_reached != True:
        if current_node.traceable == True:
            up_node = current_node.parent
            if up_node.active == True:
                current_node = up_node
            elif up_node.active == False:
                current_node = current_node
                earliest_node_reached = True
        elif current_node.traceable == False:
            earliest_node_reached = True
    return current_node

# 2. Getting sub-tree with a root vertex as the 'earliest_node'

def get_connected_children(earliest_node):
    nodes_to_isolate = []
    # Get all children
    traceable_children = earliest_node.traceable_children
    for child in traceable_children:
            if child.active == True:
                nodes_to_isolate.extend([child])       
    # Get children of children, etc via loop
    next_children_layer = []
    all_traceable_children_isolated = False
    while all_traceable_children_isolated != True:
        # Get all children of children which are traceable
        for node in traceable_children:
            next_children_layer.extend(node.traceable_children)
        # Only keep active children
        next_children_layer = [child for child in next_children_layer 
                               if child.active == True]
        if next_children_layer == []:
            all_traceable_children_isolated = True
        else:
            nodes_to_isolate.extend(next_children_layer)
            traceable_children = next_children_layer
            next_children_layer = []
            
    return nodes_to_isolate

# Note that we only consider links between active nodes. 
# Once a node becomes inactive, its links become irrelevant

# 3. Connecting previous two functions together

def get_connected_cluster(confirmed_node):
    nodes_to_isolate = []
    # Get the earliest node from which to branch out
    earliest_node = get_earliest_parent_node(confirmed_node)
    nodes_to_isolate.extend([earliest_node])
    # Get all children from the earliest node
    children_to_isolate = get_connected_children(earliest_node)
    nodes_to_isolate.extend(children_to_isolate)
    
    return nodes_to_isolate

# Function for choosing an event (birth, infection, recovery, confirmation)

events = ['birth','infection','recovery', 'confirmation']

def choose_event(total_rate, 
                 total_birth_rate, 
                 total_infection_rate, 
                 total_recovery_rate, 
                 total_confirmation_rate):

    # Event probabilities
    birth_probability = total_birth_rate/total_rate
    infection_probability = total_infection_rate/total_rate
    recovery_probability = total_recovery_rate/total_rate
    confirmation_probability = total_confirmation_rate/total_rate

    # Choose event (birth, infection, recovery, confirmation)
    probabilities = np.array([birth_probability, 
                              infection_probability, 
                              recovery_probability, 
                              confirmation_probability])
    
    # compute the cumulative sum of the probabilities
    cumulative_probabilities = np.cumsum(probabilities)

    # generate a random number
    random_number = np.random.rand()

    # find where this number would be inserted in the cumulative sum array
    index = np.searchsorted(cumulative_probabilities, random_number)
    
    chosen_event = events[index]
    
    return chosen_event

# Re-writing cumulative function using numba for time efficiency

@jit(nopython=True, fastmath=True)
def cumsum_numba(a):
    out = np.empty_like(a)
    cumsum = 0
    for i in range(a.shape[0]):
        cumsum += a[i]
        out[i] = cumsum
    return out

# Function for choosing a node (through index in a list of nodes)

def choose_index_of_node(probabilities, 
                         random_numbers, 
                         iteration_index):
    
    # cumulative sum of the probabilities
    cumulative_probabilities = cumsum_numba(probabilities)
    
    # random number between 0 and 1
    random_number = random_numbers[iteration_index]
    
    # where this number is inserted in the cumulative sum array
    index = np.searchsorted(cumulative_probabilities, random_number)
    
    return index

#####################################
# FIRST MAIN FUNCTION - simulations #
#####################################

def run_simulation(BRN_simulations = False, stopping_time = 365, 
                   max_population_BRN_simulation = 100000):
    
    # Initialisation
    current_time = 0
    nodes = [] # tracking all nodes, whether active or inactive
    active_nodes = [] # tracking active nodes 
    timeline = [] # tracks history of a disease spread
    household_sizes_array = \
                    create_size_biased_distribution_100000_values(sizes,probs)
    cluster_sizes_at_isolation = [] 
    nodes_to_isolate_batches = []
    times_of_isolation = []
    clusters = []
    
    # First node 
    start_node = Household('0', household_sizes_array[0])
    nodes.append(start_node)
    active_nodes.append(start_node)
    
    
    # Timeline tracking
    timeline_columns = ['Node id', 'Event', 'Time', 'Active nodes', 
                        'Total rate', 'Total birth rate', 
                        'Total infection rate', 
                        'Total confirmation rate', 'Total recovery rate']
    
    timeline_values = [start_node.household_id, 'birth', 0, 1, 
                       start_node.total_rate, start_node.birth_rate, 
                       start_node.infection_rate, 
                       start_node.confirmation_rate, start_node.recovery_rate]
    
    timeline.append(dict(zip(timeline_columns, timeline_values)))
    
    # First cluster
    start_cluster = Cluster(start_node, 0, 0)
    clusters.append(start_cluster)
    start_node.cluster = start_cluster
    
    # Initialise values to track progress
    population = start_node.household_size # total number of individuals 
    household_number = 1 # to track child numbers of each node
    active_nodes_cardinality = 1
    number_infected = 1
    
    # Initial rates - total
    total_rate = start_node.total_rate
    total_birth_rate = start_node.birth_rate
    total_infection_rate = start_node.infection_rate
    total_recovery_rate = start_node.recovery_rate
    total_confirmation_rate = start_node.confirmation_rate
    
    # Initial rates - list of rates for all nodes
    recovery_rates_per_node = np.array([start_node.recovery_rate])
    infection_rates_per_node = np.array([start_node.infection_rate])
    birth_rates_per_node = np.array([start_node.birth_rate])
    confirmation_rates_per_node = np.array([start_node.confirmation_rate])
    
    # for cumulative probabilities calculation
    random_numbers = np.random.rand(1000000) 
    
    iteration_index = -1
    
    while current_time < stopping_time:
        
        # If no more infected individuals 
        if number_infected == 0:
            break

        # If no more active nodes
        if active_nodes_cardinality == 0:
            break
            
        # If we are running simulations to find BRN of clusters
        if BRN_simulations == True:
            # If more than 2 clusters and first 2 clusters are inactive
            if (len(clusters) > 1) and 
               (clusters[0].active == False) and 
               (clusters[1].active == False):
                break

            if population > max_population_BRN_simulation:
                return 'death_of_cluster_undetected'
                break
        
        iteration_index += 1

        waiting_time = np.random.exponential(scale = 1/total_rate)
    
        # update time
        current_time = current_time + waiting_time
        
        # Choose event
        chosen_event = choose_event(total_rate, 
                                    total_birth_rate, 
                                    total_infection_rate, 
                                    total_recovery_rate, 
                                    total_confirmation_rate)
                
        # Create event
        if chosen_event == 'recovery':
            # choose node
            probabilities = recovery_rates_per_node / total_recovery_rate
            index = choose_index_of_node(probabilities, 
                                         random_numbers, 
                                         iteration_index)
            chosen_node = active_nodes[index]
            # apply method
            chosen_node.recovery(current_time)
            number_infected -= 1
            # updating rates
            total_rate -= chosen_node.total_rate
            total_birth_rate -= chosen_node.birth_rate
            total_infection_rate -= chosen_node.infection_rate
            total_recovery_rate -= chosen_node.recovery_rate
            total_confirmation_rate -= chosen_node.confirmation_rate
            
            chosen_node.update_attributes() 
            
            total_rate += chosen_node.total_rate
            total_birth_rate += chosen_node.birth_rate
            total_infection_rate += chosen_node.infection_rate
            total_recovery_rate += chosen_node.recovery_rate
            total_confirmation_rate += chosen_node.confirmation_rate
            
            # if no more infected individuals in the household
            if chosen_node.infected == 0:
                chosen_node.active = False

                # remove from list of rates
                recovery_rates_per_node = np.delete(recovery_rates_per_node, 
                                                    index)
                infection_rates_per_node = np.delete(infection_rates_per_node, 
                                                     index)
                birth_rates_per_node = np.delete(birth_rates_per_node, index)
                confirmation_rates_per_node = \
                                        np.delete(confirmation_rates_per_node, 
                                                  index)

                # remove from active nodes
                active_nodes.remove(chosen_node)
                active_nodes_cardinality -= 1

            elif chosen_node.infected != 0:
                # update lists of rates per node 
                recovery_rates_per_node[index] = \
                                chosen_node.recovery_rate
                infection_rates_per_node[index] = \
                                chosen_node.infection_rate
                birth_rates_per_node[index] = \
                                chosen_node.birth_rate
                confirmation_rates_per_node[index] = \
                                chosen_node.confirmation_rate
            
            # Updating timeline
            timeline_values = [chosen_node.household_id, 
                               'recovery', 
                               current_time, 
                               active_nodes_cardinality, 
                               total_rate, 
                               total_birth_rate, 
                               total_infection_rate, 
                               total_confirmation_rate, 
                               total_recovery_rate]
            
            timeline.append(dict(zip(timeline_columns, timeline_values)))
            
            
            # If we are running simulations to find BRN of clusters
            if BRN_simulations == True:
                needed_cluster = chosen_node.cluster
                if all(household.active == False for 
                       household in needed_cluster.households) == True:
                    needed_cluster.active = False

        elif chosen_event == 'infection':
            # choose node
            probabilities = infection_rates_per_node / total_infection_rate
            index = choose_index_of_node(probabilities, 
                                         random_numbers, 
                                         iteration_index)
            chosen_node = active_nodes[index]
            # apply method
            chosen_node.infection(current_time)
            number_infected += 1
            # updating rates
            total_rate -= chosen_node.total_rate
            total_birth_rate -= chosen_node.birth_rate
            total_infection_rate -= chosen_node.infection_rate
            total_recovery_rate -= chosen_node.recovery_rate
            total_confirmation_rate -= chosen_node.confirmation_rate
            
            chosen_node.update_attributes() 
            
            total_rate += chosen_node.total_rate
            total_birth_rate += chosen_node.birth_rate
            total_infection_rate += chosen_node.infection_rate
            total_recovery_rate += chosen_node.recovery_rate
            total_confirmation_rate += chosen_node.confirmation_rate
            
            # update lists of rates per node
            
            recovery_rates_per_node[index] = chosen_node.recovery_rate
            infection_rates_per_node[index] = chosen_node.infection_rate
            birth_rates_per_node[index] = chosen_node.birth_rate
            confirmation_rates_per_node[index] = chosen_node.confirmation_rate
            
            # Updating timeline
            timeline_values = [chosen_node.household_id, 'infection', 
                               current_time, active_nodes_cardinality, 
                               total_rate, total_birth_rate, 
                               total_infection_rate, 
                               total_confirmation_rate, 
                               total_recovery_rate]
            
            timeline.append(dict(zip(timeline_columns, timeline_values)))
            
        elif chosen_event == 'birth':
            # Choose node
            probabilities = birth_rates_per_node / total_birth_rate
            index = choose_index_of_node(probabilities, 
                                         random_numbers, 
                                         iteration_index)
            chosen_node = active_nodes[index]
            # For assigning correct child ids 
            child_number = len(chosen_node.children) + 1
            # apply method
            new_node = \
            chosen_node.generate_node(child_number, 
                                      current_time, 
                                      household_sizes_array[household_number])
            
            # If we are running simulations to find BRN of clusters
            if BRN_simulations == True:
                # if untraceable - new cluster
                if new_node.traceable == False:
                    parent_cluster = chosen_node.cluster
                    new_cluster = \
                        parent_cluster.create_new_cluster(new_node, 
                                                          current_time, 
                                                          parent_cluster)
                    clusters.append(new_cluster)
                    new_node.cluster = new_cluster
                    new_cluster.parent = parent_cluster

                # if traceable - new node
                elif new_node.traceable == True:
                    needed_cluster = chosen_node.cluster
                    needed_cluster.add_household(new_node)
                    new_node.cluster = needed_cluster
                
            household_number += 1
            # add to list
            active_nodes.extend([new_node])
            nodes.extend([new_node])
            population = population + new_node.household_size
            number_infected += 1
            # updating rates
            total_rate = total_rate + new_node.total_rate
            total_birth_rate += new_node.birth_rate
            total_infection_rate += new_node.infection_rate
            total_recovery_rate += new_node.recovery_rate
            total_confirmation_rate += new_node.confirmation_rate
            active_nodes_cardinality += 1
            
            # update lists of rates per node
            recovery_rates_per_node = \
                        np.append(recovery_rates_per_node, 
                                  new_node.recovery_rate)
            infection_rates_per_node = \
                        np.append(infection_rates_per_node, 
                                  new_node.infection_rate)
            birth_rates_per_node = \
                        np.append(birth_rates_per_node, 
                        new_node.birth_rate)
            confirmation_rates_per_node = \
                        np.append(confirmation_rates_per_node, 
                        new_node.confirmation_rate)
            
            # Updating timeline
            timeline_values = [new_node.household_id, 'birth', 
                               current_time, 
                               active_nodes_cardinality, 
                               total_rate, 
                               total_birth_rate, 
                               total_infection_rate, 
                               total_confirmation_rate, 
                               total_recovery_rate]
            
            timeline.append(dict(zip(timeline_columns, timeline_values)))
                    
        elif chosen_event == 'confirmation':
            # Choose node
            probabilities = confirmation_rates_per_node / \
                            total_confirmation_rate
            index = choose_index_of_node(probabilities, 
                                         random_numbers, 
                                         iteration_index)
            chosen_node = active_nodes[index]
            
            # If we are running simulations to find BRN of clusters
            if BRN_simulations == True:
                # make cluster inactive
                cluster_to_isolate = chosen_node.cluster
                cluster_to_isolate.active = False
            # apply method
            nodes_to_isolate = get_connected_cluster(chosen_node)
            nodes_to_isolate_batches.append(nodes_to_isolate)
            count_nodes_to_isolate = 0
            times_of_isolation.append(current_time)
            for node in nodes_to_isolate:
                count_nodes_to_isolate += 1
                number_infected -= node.infected
                if node == chosen_node:
                    index = active_nodes.index(node)
                    node.isolation(current_time, True)
                    recovery_rates_per_node = \
                                np.delete(recovery_rates_per_node, 
                                          index)
                    infection_rates_per_node = \
                                np.delete(infection_rates_per_node, 
                                index)
                    birth_rates_per_node = \
                                np.delete(birth_rates_per_node, 
                                index)
                    confirmation_rates_per_node = \
                                np.delete(confirmation_rates_per_node, 
                                index)
                    
                    # remove from rates, as not in the active_nodes list
                    total_rate = total_rate - node.total_rate
                    total_birth_rate -= node.birth_rate
                    total_infection_rate -= node.infection_rate
                    total_recovery_rate -= node.recovery_rate
                    total_confirmation_rate -= node.confirmation_rate

                    # remove from the list of active nodes
                    active_nodes.remove(node)
                    active_nodes_cardinality -= 1
                    
                    # Updating timeline
                    timeline_values = [node.household_id, 
                                       'confirmation_and_isolation', 
                                       current_time, 
                                       active_nodes_cardinality, 
                                       total_rate, 
                                       total_birth_rate, 
                                       total_infection_rate, 
                                       total_confirmation_rate, 
                                       total_recovery_rate]

                    timeline.append(dict(zip(timeline_columns, 
                                             timeline_values)))
                    
                else:
                    index = active_nodes.index(node)
                    node.isolation(current_time, False)
                    # update lists of rates per node 
                    recovery_rates_per_node = \
                                np.delete(recovery_rates_per_node, 
                                index)
                    infection_rates_per_node = \
                                np.delete(infection_rates_per_node, 
                                index)
                    birth_rates_per_node = \
                                np.delete(birth_rates_per_node, 
                                index)
                    confirmation_rates_per_node = \
                                np.delete(confirmation_rates_per_node, 
                                index)
                    
                    # remove from rates, as not in the active_nodes list
                    total_rate = total_rate - node.total_rate
                    total_birth_rate -= node.birth_rate
                    total_infection_rate -= node.infection_rate
                    total_recovery_rate -= node.recovery_rate
                    total_confirmation_rate -= node.confirmation_rate

                    # remove from the list of active nodes
                    active_nodes.remove(node)
                    active_nodes_cardinality -= 1
                    
                    # Updating timeline
                    timeline_values = [node.household_id, 'isolation', 
                                       current_time, 
                                       active_nodes_cardinality, 
                                       total_rate, 
                                       total_birth_rate, 
                                       total_infection_rate, 
                                       total_confirmation_rate, 
                                       total_recovery_rate]

                    timeline.append(dict(zip(timeline_columns, 
                                             timeline_values)))
                    
                # Appending size of an isolated cluster    
            cluster_sizes_at_isolation.append(count_nodes_to_isolate)
                    
        # If no more infected individuals 
        if number_infected == 0:
            break

        # If no more active nodes
        if active_nodes_cardinality == 0:
            break
        
        if population > 100000:
            break
    
    # Convert timeline results to dataframe for readability
    timeline = pd.DataFrame(timeline)
        
    results = nodes, active_nodes, timeline, 
              cluster_sizes_at_isolation, nodes_to_isolate_batches, 
              times_of_isolation, clusters
            
    return results
