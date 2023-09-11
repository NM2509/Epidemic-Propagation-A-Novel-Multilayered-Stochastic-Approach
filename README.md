# MSc-Dissertation-Anastasia-Malakhova
Dissertation for MSc in Statistical Science at the University of Oxford. Supervised by Prof. Julien Berestycki and Dr. Félix Foutel-Rodier. Title: Incorporating Household Structure into Branching Processes for Epidemic Propagation: A Novel Multilayered Stochastic Approach with SIR Transmission and Cluster Isolation.

This work presents a new epidemiological model that is based on a branching process with an addition of household structure to better capture non-random patterns of contact between individuals. The code provided in this repository has been used for simulations and analysis of such model. 


File '8. Simulations - main function' is the main function which runs a simulation of spread of a disease, with nodes representing households, 
and clusters - households wuth traceable edges between them. In order to run, this function requires all functions defined in files 0-7. 

File '9. R0 estimation - main function' is the main function used for section '6 Basic Reproduction Number (R0)' of the dissertation, and below. This function provides an unbiased estimate of the Basic Reproduction Number, given default parameter inputs. This function requires other functions defined in file 0 in order to run. 

File 0
