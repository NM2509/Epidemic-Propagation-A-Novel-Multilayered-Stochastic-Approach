# MSc Dissertation - Anastasia Malakhova

## Incorporating Household Structure into Branching Processes for Epidemic Propagation: A Novel Multilayered Stochastic Approach with SIR Transmission and Cluster Isolation

This repository contains the codebase for my MSc Dissertation in Statistical Science at the University of Oxford. The research presents a new epidemiological model that is based on a branching process with an addition of household structure to better capture non-random patterns of contact between individuals. The code provided in this repository has been used for simulations and analysis of such model. 

### Supervisors: 
Prof. Julien Berestycki \
Dr. Félix Foutel-Rodier 

### Dependencies: 
All requirements are in the requirements.txt file

## File Descriptions: 

| Filename       | Description     |
|----------------|---------------------------------------------------------------------------------------------------|
| defining_parameters.py         | Defines functions for model inputs and their default values                                       |
| nodes_class.py         | Defining `Household` class                                                                        |
| clusters_class.py         | Defining `Cluster` class. We only use this class when running simulations to determine the average number of child clusters, as it substantially increases run time of simulations.                                |
| get_connected_cluster.py         | Functions to identify households for isolation (isolation of a cluster)                                 |
| get_cluster_by_id.py         | Function to get a cluster by its ID. Only used if we are running simulations to get the average number of child clusters                                  |
| choose_event.py         | Choosing an event out of 'birth', 'recovery, 'detection', 'infection'                                  |
| choose_node.py         | Choosing a node that a previously chosen event will apply to                                   |
| cumulative_sum.py         | Faster cumulative sum function using numba                                   |
| main.py         | Main simulation function. Requires all the files listed above                                   |
| r_zero_estimation.py         | Main function for section 6 of the dissertation. This function provides an unbiased estimate of the Basic Reproduction Number, given parameter inputs. Requires file 0                                  |
| ks_statistic.py         | Code for the Kolmogorov-Smirnov test for section 7 of the dissertation                                  |
| requirements.txt | Requirements for the code to run |
|  Other files      |           Correspond to Figures and Tables in the dissertation                             |


## How to Run

1. **Setup**: 
    - Clone the repository to your local machine
    - Ensure you've installed all required dependencies (see the "Dependencies" section)

2. **Executing the Code**: 
    - Navigate to the project directory.
    - Run main.py file to generate a simulation
    - Run r_zero_estimation.py file to generate an R0 estimation
    - Run ks_statistic file to obtain results for section 7 of the dissertation









