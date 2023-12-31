######################################################################################################
# Note that for this function, all previous functions in files 0-7 are needed.                       #
# This function outputs results of a simulation, given specified parameters in                       #
# '0. Defining parameters'. The output includes:                                                     #
#                                                                                                    #
# * nodes - a list of nodes at the end of the simulation, both active and inactive                   #
# * active_nodes - a list of active nodes at the end of the simulation                               #
# * timeline - times of each event, corresponding affected node and corresponding rates              #
# * cluster_sizes_at_isolation - a list of cluster sizes at isolation                                #
# * nodes_to_isolate_batches - list of lists of nodes that are being isolated after detection occurs #
# * times_of_isolation - times at which clusters are isolated                                        #
# * clusters - list of clusters (only retuns results if BRN_simulations parameter is set to True)    #
######################################################################################################
 
# Notes on inputs:

# * BRN_simulations - default is 'False'. Set it to 'True' if working with clusters (i.e. when we want 'clusters' output)
# * stopping_time - set to a default of one year, i.e. 365. Can be changed to any other value
# * max_population_BRN_simulation - stopping simulation when number of individual reaches this limit - set to a default of 100,000

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

#######################
from defining_parameters import *
from nodes_class import *
from clusters_class import *
from choose_event import *
from choose_node import *
from get_connected_cluster import *
from cumulative_sum import *
from get_cluster_by_id import *


##############
# Simulation #
##############

def run_simulation(BRN_simulations = False, stopping_time = 365, 
                   max_population_BRN_simulation = 100000):
    
    # Initialisation
    current_time = 0
    nodes = [] # tracking all nodes, whether active or inactive
    active_nodes = [] # tracking active nodes 
    timeline = [] # tracks history of a disease spread
    household_sizes_array = create_size_biased_distribution_100000_values(sizes,probs)
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
                recovery_rates_per_node = np.delete(recovery_rates_per_node, index)
                infection_rates_per_node = np.delete(infection_rates_per_node, index)
                birth_rates_per_node = np.delete(birth_rates_per_node, index)
                confirmation_rates_per_node = np.delete(confirmation_rates_per_node, index)

                # remove from active nodes
                active_nodes.remove(chosen_node)
                active_nodes_cardinality -= 1

            elif chosen_node.infected != 0:
                # update lists of rates per node 
                recovery_rates_per_node[index] = chosen_node.recovery_rate
                infection_rates_per_node[index] = chosen_node.infection_rate
                birth_rates_per_node[index] = chosen_node.birth_rate
                confirmation_rates_per_node[index] = chosen_node.confirmation_rate
            
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
            new_node = chosen_node.generate_node(child_number, 
                                      current_time, 
                                      household_sizes_array[household_number])
            
            # If we are running simulations to find BRN of clusters
            if BRN_simulations == True:
                # if untraceable - new cluster
                if new_node.traceable == False:
                    parent_cluster = chosen_node.cluster
                    new_cluster = parent_cluster.create_new_cluster(new_node, 
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
            recovery_rates_per_node = np.append(recovery_rates_per_node, 
                                  new_node.recovery_rate)
            infection_rates_per_node = np.append(infection_rates_per_node, 
                                  new_node.infection_rate)
            birth_rates_per_node = np.append(birth_rates_per_node, 
                        new_node.birth_rate)
            confirmation_rates_per_node = np.append(confirmation_rates_per_node, 
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
            probabilities = confirmation_rates_per_node / total_confirmation_rate
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
                    recovery_rates_per_node = np.delete(recovery_rates_per_node, index)
                    infection_rates_per_node = np.delete(infection_rates_per_node, index)
                    birth_rates_per_node = np.delete(birth_rates_per_node, index)
                    confirmation_rates_per_node = np.delete(confirmation_rates_per_node, index)
                    
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
                    recovery_rates_per_node = np.delete(recovery_rates_per_node, index)
                    infection_rates_per_node = np.delete(infection_rates_per_node, index)
                    birth_rates_per_node = np.delete(birth_rates_per_node, index)
                    confirmation_rates_per_node = np.delete(confirmation_rates_per_node, index)
                    
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
