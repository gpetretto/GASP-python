# Outline of the algorithm
import yaml
import sys
import os
import classes

# get the pash to the input file (in yaml format)
#input_file = os.path.abspath(sys.argv[1]) 

# parse the input file as nested dictionaries
#with open(input_file, 'r') as f:
#    parameters = yaml.load(f)

#with open('/Users/benjaminrevard/GASPy/gaspy/src/gaspy_input.yaml', 'r') as f:
#    parameters = yaml.load(f)


with open('/n/srv/brevard/python_GA/gaspy/src/gaspy_input.yaml', 'r') as f:
    parameters = yaml.load(f)

    
# make the composition space object
try:
    composition_space = classes.CompositionSpace(parameters['CompositionSpace'])
except KeyError:
    print("Input file must contain a CompositionSpace block.")

# get the objective function (energy per atom or phase diagram) from the composition space
objective_function = composition_space.inferObjectiveFunction()

# make the constraints object
try:
    constraints = classes.Constraints(parameters['Constraints'], composition_space, objective_function)
except KeyError:
    # if no Constraints block is given in the input file, then just use default values for everything
    constraints = classes.Constraints('default', composition_space, objective_function)

# make the geometry object
try:
    geometry = classes.Geometry(parameters['Geometry'])
except KeyError:
    # if no Geometry block is given in the input file, then just use default values for everything
    geometry = classes.Geometry('default')
    


# make the development object

# make the redundancy_guard object

# make the creator objects

#for i in parameters['InitialPopulation']:
#    if i == 'random':
#        print('make RandomOrgCreator')
#    elif i == 'fromPoscars':
#        print('make PoscarOrgCreator')
        
    #print parameters['InitialPopulation'][i]

# construct the creators and put them in a list
#creators = []


'''


# get the parameters from the input file, and store them as nested dictionaries
parameters_parser = ParametersParser(path_to_input_file)
dict_of_parameters = parameters_parser.parse()

# create objects that will be used throughout the search by passing the appropriate dictionary 
# of input data to the constructor.

# make the organism creator objects (from poscars, random, etc.) and put them in a list
organism_creators = []
for name in dict_of_parameters['Initial Population']
    Name = str(name)
    organism_creators.append(Name(name))
# TODO: sort the list of creators so that the num_attempts ones are at the front and the num_successes ones are
# at the back

# create variation objects (Mutation, Mating, etc.) and put them in a list
variations = []
for name in dict_of_parameters['Variations']:
    Name = str(name)
    variations.append(Name(name))

# create other objects we'll need
id_generator = IDGenerator()    # id generator - do we need this up here? Not sure...
structure_matcher = pymatgen.analysis.structure_matcher.StructureMatcher(input)
redundancy_guard = RedundancyGuard(structure_matcher, other_inputs)
development = Development(niggli_params, constraint_params)
offspring_generator = OffspringGenerator(variations, development, redundancy_guard, 10000)
energy_calculator = "energy code name" + "EnergyCalculator"(energy_code_params)
waiting_queue = deque()         # queue to hold the organisms that have finished their energy calculations and are
                                # waiting to be added to the pool
whole_pop = []                  # holds every organism that has been submitted for energy calculation, both relaxed and unrelaxed
others?

# create the initial population
initial_population = InitialPopulation(whole_pop)
threads = []  # list of threads to do the energy calculations
for creator in organism_creators:
    while not creator.isFinished:
        # start by making N threads
        if len(threads) < N:
            new_organism = creator.create_organism() # this handles development and redundancy checking, but could fail for poscar creator...
            if new_organism != None:
                new_organism.structure = geometry.pad(new_organism.structure) # for bulk search, this does nothing except rotate into principal directions
                thread = Thread(target=energy_calculator.doEnergyCalculation, args=(new_organism))
                thread.start()
                threads.append(thread)
        else:
            # check for dead threads
            for thread in threads:
                if not thread.isAlive:
                    # TODO: need to figure out how to get the return value from a dead thread
                    relaxed_org = thread.return_value  
                    if relaxed_org != None:
                        relaxed_org.structure = geometry.unpad(relaxed_org.structure) # for bulk search, this does nothing except rotate into principal directions
                        developed_org = development.develop(relaxed_org)
                        if developed_org != None:
                            redundant_org = redundancy_guard.checkRedundancy(developed_org, whole_pop)
                            if redundant_org != None:
                                if redundant_org.isActive and redundant_org.value > developed_org.value:
                                    initial_population.replaceOrganism(redundant_org, developed_org)
                            else:
                                initial_population.add(developed_org)
                                if creator.when_stop == "successes": # update status of success-based creators
                                    creator.updateStatus()
                                
                    # remove the dead thread and make another one
                    threads.remove(thread)
                    new_organism = creator.create_organism() # this handles development and redundancy checking, but could fail for poscar creator...
                    if new_organism != None:
                        new_organism.structure = geometry.pad(new_organism.structure)
                        thread = Thread(target=energy_calculator.doEnergyCalculation, args=(new_organism))
                        thread.start()
                        threads.append(thread)


# create the pool
pool = Pool(initial_population, other args)
threads = []  # list of threads to do the energy calculations (overwrite the old list used in initial population)

# create the initial batch of N offspring organisms and submit them for energy calculations
for i in range(0, N):
    unrelaxed_offspring = offspring_generator.makeOffspringOrganism(pool, whole_pop)
    unrelaxed_offspring.structure = geometry.pad(unrelaxed_offspring.structure) 
    thread = Thread(target=energy_calculator.doEnergyCalculation, args=(new_organism))
    thread.start()
    threads.append(thread)

# continue the search until stopping criteria are met
while the stopping criteria are not met:
    # check for dead threads
    for thread in threads:
        if not thread.isAlive:
            # TODO: need to figure out how to get the return value from a dead thread
            relaxed_org = thread.return_value  
            if relaxed_org != None:
                relaxed_org.structure = geometry.unpad(relaxed_org.structure) 
                developed_org = development.develop(relaxed_org)
                if developed_org != None:
                    redundant_org = redundancy_guard.checkRedundancy(developed_org, whole_pop)
                    if redundant_org != None and redundant_org.isActive and redundant_org.value > developed_org.value:
                            pool.replaceOrganism(redundant_org, developed_org)
                    else:
                        pool.add(developed_org)
                        # check if we've added enough new offspring orgs to the pool that we can trim off the initial
                        # population orgs from the queue. poolSize and numPromoted are user inputs.
                        if (pool.numAdds == (poolSize - numPromoted)):
                            for i in range(0, len(pool.queue) - (poolSize - numPromoted)):
                                pool.queue.popleft()
                
                        # check if we've already added more than enough offspring to the pool to allow trimming off the 
                        # orgs from the initial population, in which case it has already happened, and we just need to
                        # remove one organism from the pool
                        elif (pool.numAdds > (poolSize - numPromoted)):
                            pool.queue.popleft()
                                                
            # remove the dead thread and make another one
            threads.remove(thread)
            pool.calculateFitnesses()
            pool.calculateSelectionProbs()
            offspring = offspring_generator.makeOffspringOrganism(pool, whole_pop) # this handles development and redundancy
            offspring.structure = geometry.pad(offspring.structure) 
            thread = Thread(target=energy_calculator.doEnergyCalculation, args=(offspring))
            thread.start()
            threads.append(thread)

'''
