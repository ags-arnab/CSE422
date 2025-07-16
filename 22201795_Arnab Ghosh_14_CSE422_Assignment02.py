import random

# TASK 1
STARTING_CAPITAL = 1000
PRICE_MOVEMENTS = [-1.2, 3.4, -0.8, 2.1, -2.5, 1.7, -0.3, 5.8, -1.1, 3.5]
POPULATION_SIZE = 4
MAX_GENERATIONS = 10
MUTATION_RATE = 0.05

def calculate_fitness(strategy, capital, price_history):
    current_capital = capital
    for price_change in price_history:
        trade_amount = current_capital * (strategy['trade_size'] / 100)
        if price_change <= -strategy['stop_loss']:
            loss = trade_amount * (strategy['stop_loss'] / 100)
            current_capital -= loss
        elif price_change >= strategy['take_profit']:
            gain = trade_amount * (strategy['take_profit'] / 100)
            current_capital += gain
        else:
            current_capital += trade_amount * (price_change / 100)
    return current_capital - capital

def create_initial_population(size):
    population = []
    for i in range(size):
        strategy = {
            "stop_loss": round(random.uniform(1, 99), 1),
            "take_profit": round(random.uniform(1, 99), 1),
            "trade_size": round(random.uniform(1, 99), 1)
        }
        population.append(strategy)
    return population

def select_parents(population):
    return random.sample(population, 2)

def crossover(parent1, parent2):
    offspring = {}
    genes = list(parent1.keys())
    split_point = random.randint(1, len(genes)-1)
    for i in range(split_point):
        offspring[genes[i]] = parent1[genes[i]]
    for i in range(split_point, len(genes)):
        offspring[genes[i]] = parent2[genes[i]]
    return offspring

def mutate(strategy, mutation_rate):
    if random.random() < mutation_rate:
        gene = random.choice(list(strategy.keys()))
        new_value = strategy[gene] + random.uniform(-0.5, 0.5)
        strategy[gene] = max(1, min(99, new_value))

def evaluate_population(population, capital, price_history):
    evaluated = [(strategy, calculate_fitness(strategy, capital, price_history)) 
                 for strategy in population]
    return sorted(evaluated, key=lambda x: x[1], reverse=True)

def evolve(generations, population_size, capital, price_history, mutation_rate):
    global initial_population
    initial_population = create_initial_population(population_size)
    
    # Print initial population
    # print("\nInitial Population:")
    # for i, strategy in enumerate(initial_population):
    #     fitness = calculate_fitness(strategy, capital, price_history)
    #     print(f"Strategy {i+1}: {strategy} - Fitness: {round(fitness, 2)}")
    
    population = initial_population.copy()
    for i in range(generations):
        evaluated_pop = evaluate_population(population, capital, price_history)
        new_population = [evaluated_pop[0][0]]
        while len(new_population) < population_size:
            parent1, parent2 = select_parents([s[0] for s in evaluated_pop])
            offspring = crossover(parent1, parent2)
            mutate(offspring, mutation_rate)
            new_population.append(offspring)
        population = new_population
    final_evaluation = evaluate_population(population, capital, price_history)
    best_strategy = final_evaluation[0][0]
    best_fitness = final_evaluation[0][1]
    return best_strategy, best_fitness

best_strategy, final_profit = evolve(
    MAX_GENERATIONS,
    POPULATION_SIZE,
    STARTING_CAPITAL,
    PRICE_MOVEMENTS,
    MUTATION_RATE
)

print("Best Strategy:", best_strategy)
print("Final Profit:", round(final_profit, 2))

# TASK 2
# def strategy_to_string(strategy):
#     stop_loss_str = f"{int(strategy['stop_loss']):02d}"
#     take_profit_str = f"{int(strategy['take_profit']):02d}"
#     trade_size_str = f"{int(strategy['trade_size']):02d}"
#     return stop_loss_str + take_profit_str + trade_size_str

# def string_to_strategy(chromosome_str):
#     stop_loss = int(chromosome_str[0:2])
#     take_profit = int(chromosome_str[2:4])
#     trade_size = int(chromosome_str[4:6])
#     return {
#         "stop_loss": stop_loss,
#         "take_profit": take_profit,
#         "trade_size": trade_size
#     }

# parent1, parent2 = random.sample(initial_population, 2)
# parent1_str = strategy_to_string(parent1)
# parent2_str = strategy_to_string(parent2)


# def perform_two_point_crossover(string1, string2):
#     first_cut = random.randint(1, len(string1)-2)
#     second_cut = random.randint(first_cut+1, len(string1)-1)
    
#     child1 = string1[:first_cut] + string2[first_cut:second_cut] + string1[second_cut:]
#     child2 = string2[:first_cut] + string1[first_cut:second_cut] + string2[second_cut:]
    
#     return child1, child2, first_cut, second_cut

# child1_str, child2_str, cut_point_1, cut_point_2 = perform_two_point_crossover(parent1_str, parent2_str)

# # print("\nParents:")
# # print(f"Parent 1 Strategy: {parent1}")
# # print(f"Parent 2 Strategy: {parent2}")

# print("Crossover points:")
# print(f"Parent 1: {parent1_str}")
# print(f"Parent 2: {parent2_str}")
# print(f"Cut 1: {cut_point_1}")
# print(f"Cut 2: {cut_point_2}")
# print(f"Child 1: {child1_str}")
# print(f"Child 2: {child2_str}")
