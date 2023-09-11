#####################################################
# NODES - defining class - each node is a household #
#####################################################

class Household:
    def __init__(self, household_id, household_size):
        # Attributes - core information
        self.household_id = household_id
        self.household_size = household_size
        
        # Attributes - cluster
        self.cluster = None
        
        # Attributes - children
        self.children = []
        self.traceable_children = []
        
        # Attributes - parent
        self.parent = None
        
        # Attributes - traceability to parent
        self.traceable = edge_status(household_id)
        
        # Attributes - times
        self.child_times = []
        self.traceable_child_times = []
        self.infected_times = []
        self.recovered_times = []
        self.confirmation_time = [] 
        self.isolation_time = [] 
        self.event_times = []
        
        # Arrtibutes - active / inactive
        self.active = True
        
        # Attributes - S I R (initial)
        self.susceptible = self.household_size - 1
        self.infected = 1
        self.recovered = 0
        
        # Attributes - Rates
        self.infection_rate = infection_rate_function(self.susceptible, 
                                                      self.infected, 
                                                      self.household_size)
        self.recovery_rate = recovery_rate_function(self.infected)
        self.birth_rate = birth_rate_function(self.infected)
        self.confirmation_rate = confirmation_rate_function(self.infected)
        self.total_rate = self.infection_rate + self.recovery_rate + 
                          self.birth_rate + self.confirmation_rate
    
    # Method - generate other nodes
    def generate_node(self, number, time, size):
        if self.active == True: 
            new_node = Household(str(self.household_id) +
                                 "_" + str(number), size)
            new_node.parent = self
            self.children.append(new_node)
            self.child_times.append(time)
            if new_node.traceable == True:
                self.traceable_children.append(new_node)
                self.traceable_child_times.append(time)
            self.event_times.append((time, 'birth'))
        elif self.active == False:
            pass
        return new_node
    
    # Method - infection of individual
    def infection(self, time):
        self.susceptible = self.susceptible - 1
        self.infected = self.infected + 1
        self.recovered = self.recovered
        
        self.infected_times.append(time)
        self.event_times.append((time, 'infection'))
        return self
    
    # Method - recovery of individual
    def recovery(self, time):
        self.susceptible = self.susceptible
        self.infected = self.infected - 1
        self.recovered = self.recovered + 1
        
        self.recovered_times.append(time)
        self.event_times.append((time,'recovery'))
        return self
    
    # Method - confirmation of a node 
    def isolation(self, time, confirmed_node):
        self.active = False
        # if this was the node that was initially confirmed
        if confirmed_node == True:
            self.confirmation_time.append(time)
            self.isolation_time.append(time)
            self.event_times.append((time,'confirmation_and_isolation'))
        elif confirmed_node == False:
            self.isolation_time.append(time)
            self.event_times.append((time,'isolation'))            
        return self
    
    # Method - updating rates 
    def update_attributes(self):
        self.infection_rate = infection_rate_function(self.susceptible, 
                                                      self.infected, 
                                                      self.household_size)
        self.recovery_rate = recovery_rate_function(self.infected)
        self.birth_rate = birth_rate_function(self.infected)
        self.confirmation_rate = confirmation_rate_function(self.infected)
        self.total_rate = self.infection_rate + self.recovery_rate + 
                          self.birth_rate + self.confirmation_rate
