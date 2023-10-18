# MSc Dissertation - Anastasia Malakhova

## Incorporating Household Structure into Branching Processes for Epidemic Propagation: A Novel Multilayered Stochastic Approach with SIR Transmission and Cluster Isolation

This repository contains the codebase for my MSc Dissertation in Statistical Science at the University of Oxford. The research presents a new epidemiological model that is based on a branching process with an addition of household structure to better capture non-random patterns of contact between individuals. The code provided in this repository has been used for simulations and analysis of such model. 

### Supervisors: 
Prof. Julien Berestycki \
Dr. Félix Foutel-Rodier 

### Dependencies: 
To run the code from this repository, please ensure you have the following Python libraries installed:

#### Core Libraries
* numpy
* pandas

#### Visualization Libraries
* matplotlib
* seaborn

#### Optimization and Statistics
* scipy
* sympy

#### Performance and Profiling
* cProfile
* pstats
* numba

#### Utilities
* random
* warnings
* time



## Files Description: 

| Filename       | Description     |
|----------------|---------------------------------------------------------------------------------------------------|
| File 0         | Defines functions for model inputs and their default values                                       |
| File 1         | Defining `Household` class                                                                        |
| File 2         | Defining `Cluster` class. We only use this class when running simulations to determine the average number of child clusters, as it substantially increases run time of simulations.                                |
| File 3         | Functions to identify households for isolation (isolation of a cluster)                                 |
| File 4         | Function to get a cluster by its ID. Only used if we are running simulations to get the average number of child clusters                                  |
| File 5         | Choosing an event out of 'birth','recovery','detection','infection'                                  |
| File 6         | Choosing a node that a previously chosen event will apply to                                   |
| File 7         | Faster cumulative sum function using numba                                   |
| File 8         | Main simulation function. Requires files 0-7                                   |
| File 9         | Main function for section 6 of the dissertation. This function provides an unbiased estimate of the Basic Reproduction Number, given parameter inputs. Requires file 0                                  |
| KS Statistic         | Code for the Kolmogorov-Smirnov test for section 7 of the dissertation                                  |
|  Other files      |           Correspond to Figures and Tables in the dissertation                             |






