######################################## 
# R0 estimation                        #
#                                      #
# This function is used in section     #
# 6. Basic Reproduction Number (R0).   #
# The function outputs 100 estimated   #
# BRN numbers given default parameters #
########################################

def R_0_estimation(Global_rate, 
                   Recovery_rate, 
                   Local_rate, 
                   Confirmation_rate, 
                   Traceable_probability, 
                   size_biased_weights, 
                   sizes):
    
    # Save integrals to calculate their expectation
    integrals = []
    Basic_Reproduction_Numbers = []

    for k in range(100):
        # 100 is the number of clusters we will grow to calculate one BRN
        for _ in range(100):

            dt = 0.01
            T = 1000
            times = np.arange(0, T, dt)

            # Initialise
            C_values = [1]
            I_values = [1]
            Ii_values = [[1]]
            Ri_values = [[0]]
            R_values = [0]
            D_value = 0
            probabilities = size_biased_weights
            household_sizes = [np.random.choice(sizes, p=probabilities)]

            while I_values[-1] != 0:
                C_current = C_values[-1] 
                I_current = I_values[-1]
                Ii_current = Ii_values[-1]
                Ri_current = Ri_values[-1]

                # Update C(t)
                dC = np.random.poisson(Global_rate * 
                                       Traceable_probability * 
                                       I_current * dt)
                C_values.append(C_current + dC)

                # New households
                for _ in range(dC):
                    household_sizes.append(np.random.choice(sizes, 
                                                            p = probabilities))
                    Ii_current.append(1)
                    Ri_current.append(0)

                Ii_next = []
                Ri_next = []

                # For every household
                for i in range(C_current + dC):  
                    # quantities for household i
                    size_i = household_sizes[i]
                    Ii_i = Ii_current[i]
                    Ri_i = Ri_current[i]

                    # Update R_i(t)
                    dRi = np.random.poisson(Recovery_rate * Ii_i * dt)
                    # making sure we don't recover more individuals 
                    # than we have infected
                    if dRi > Ii_i:
                        dRi = Ii_i
                    Ri_next.append(Ri_i + dRi)

                    # Determine the infection rate
                    if size_i - Ii_i - Ri_i > 0:
                        infection_rate = Local_rate * Ii_i * 
                        (size_i - Ii_i - Ri_i) / (size_i - 1)
                        dIi = np.random.poisson(infection_rate * dt)
                    else:
                        dIi = 0
                    # Update number of infected
                    Ii_next.append(Ii_i + dIi - dRi)

                # Update with a new list of Ii_values and Ri_values    
                Ii_values.append(Ii_next)
                Ri_values.append(Ri_next)

                # Update total number of infected in a cluster
                I_values.append(sum(Ii_values[-1]))

                # Check if detected
                D_value = np.random.poisson(Confirmation_rate * 
                                            I_values[-1] * dt)

                if D_value == 0:
                    pass
                else:
                    # stop running the loop as cluster is isolated
                    I_values.append(0)
                    break 

            integral_I = np.trapz(I_values, times[0:len(I_values)])
            integrals.append(integral_I)

        # Appending one BRN    
        expected_integral = np.array(integrals).mean()
        BRN = Global_rate * (1-Traceable_probability) * expected_integral
        Basic_Reproduction_Numbers.append(BRN)
    return Basic_Reproduction_Numbers
