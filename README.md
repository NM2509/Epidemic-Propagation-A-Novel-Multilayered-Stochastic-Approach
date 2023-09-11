# MSc-Dissertation-Anastasia-Malakhova
Dissertation for MSc in Statistical Science at the University of Oxford. Supervised by Prof. Julien Berestycki and Dr. Félix Foutel-Rodier. Title: Incorporating Household Structure into Branching Processes for Epidemic Propagation: A Novel Multilayered Stochastic Approach with SIR Transmission and Cluster Isolation.

This work presents a new epidemiological model that is based on a branching process with an addition of household structure to better capture non-random patterns of contact between individuals. The code provided in this repository has been used for simulations and analysis of such model. 

** Description of files: **

Libraries file - lists all libraries required to run the code.

File 0 - defines functions needed for the use of model parameters. It additionally sets those parameters to default values.

File 1 - defines a class called 'Household'. Each household has a range of attributes, such as the number of susceptible, infected, and recovered
individuals. It additionally has methods to give birth, infect, recover, isolate, and update attributes. 

File 2 - defines a class called 'Cluster', which corresponds to clusters of households. We only use this class when running simulations to determine the average number of child clusters, as it substantially increases run time of simulations. 

File 3 - defines three functions which are needed in order to obtain all households to isolate in case of a detection. This would correspond to a cluster. 

File 4 - if we are running simulations to get the average number of child clusters, this function gets a cluster by its id.

File 5 - choosing an event out of 'birth','recovery','detection','infection'.

File 6 - choosing a node that a previously chosen event will apply to. 

File 7 - redefining cumulative sum function using numba for increased computational speed.

File 8 - is the main function which runs a simulation of a spread of a disease. In order to run, this function requires all functions defined in files 0-7. 

File 9 - is the main function used for section '6 Basic Reproduction Number (R0)' of the dissertation, and below. This function provides an unbiased estimate of the Basic Reproduction Number, given parameter inputs. This function requires other functions defined in file 0 in order to run. 

KS Statistic - the code used to calculate the p-value of Kolmogorov-Smirnov test when checking whether the size of clusters prior to their isolation follow a geometric distribution. 

The other files are as per the corresponding Figures and Tables in the Dissertation.




