###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cow_dict = {}
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(',')
            cow_dict[key] = int(val)

    return cow_dict
   
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cow_list = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    
    list_index = 0
    trips = []
    transported = []
    while len(cow_list) > 0:
        totalWeight = 0
        trips.append([])
        transported.append([])
        for (cow, weight) in cow_list:
            if (totalWeight + weight) <= limit:
                trips[list_index].append(cow)
                totalWeight += weight
                transported[list_index].append((cow, weight))
        for x in transported[list_index]:
            cow_list.pop(cow_list.index(x))
        list_index += 1
    return trips
    
def test_greedy(filename):
    result = greedy_cow_transport(load_cows(filename))
    return result

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    trips = []
    cow_list = []
    for key, val in cows.items():
        cow_list.append((key, val))
    
    output = get_partitions(cow_list)
    combs = []
    for i in output:
        combs.append(i)
    
    overweight = []
    #combs example: [[[('Herman', 7), ('Betsy', 9), ('Maggie', 3)]], [[('Herman', 7), ('Betsy', 9)], [('Maggie', 3)]], [[('Betsy', 9), ('Maggie', 3)], [('Herman', 7)]], [[('Betsy', 9)], [('Herman', 7), ('Maggie', 3)]], [[('Betsy', 9)], [('Maggie', 3)], [('Herman', 7)]]]
    for comb in combs: #comb example: [[('Herman', 7), ('Betsy', 9)], [('Maggie', 3)]]
        for trip in comb: #i example: [('Herman', 7), ('Betsy', 9)]
            totalWeight = 0
            for cow in trip: #cow example: ('Herman', 7)
                totalWeight += cow[1]
            if totalWeight > 10:
                overweight.append(comb)
       
    for x in overweight:
        if x in combs:
            combs.remove(x)
    
    list_index = 0
    for comb in combs:
        trips.append([])
        sub_index = 0
        for trip in comb:
            trips[list_index].append([])
            for cow in trip:
                trips[list_index][sub_index].append(cow[0])
            sub_index += 1
        list_index += 1   

    shortest = min(trips, key=len)
    
    return shortest
    # TODO: Your code here
    
def test_brute_force(filename):
    result = brute_force_cow_transport(load_cows(filename))
    return result
        
# Problem 4
def compare_cow_transport_algorithms(filename):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start_greedy = time.time()
    test_greedy(filename)
    end_greedy = time.time()
    print(test_greedy(filename))
    print("Run time of Greedy is", end_greedy - start_greedy)
    
    start_brute_force = time.time()
    test_brute_force(filename)
    end_brute_force = time.time()
    print(test_brute_force(filename))
    print("Run time of Brute Force is", end_brute_force - start_brute_force)

    return

if __name__ == '__main__':
    filename = "ps1_cow_data.txt"
    compare_cow_transport_algorithms(filename)
    

