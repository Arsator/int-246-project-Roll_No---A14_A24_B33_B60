# GENETIC ALGORITHM
from tkinter import *
from tkinter.ttk import *
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.animation import FuncAnimation
#import matplotlib.animation as animation


import numpy
import string
import matplotlib.pyplot as plt
import matplotlib.animation
#import matplotlib
import random

numpy.random.seed(1)

N = 25

_nodes = [(random.uniform(-400, 400), random.uniform(-400, 400)) for _ in range(0, 25)]
xx = [i[0] for i in _nodes]
yy = [i[1] for i in _nodes]

# Generation of labels and random coordinates for N cities
CITY_LABELS = list(range(N))
#CITY_COORD = numpy.random.randint(0, 200, (N, 2))
#CITY_COORD=numpy.array([(random.uniform(-400, 400), random.uniform(-400, 400)) for _ in range(0, 25)])
CITY_COORD=numpy.array(_nodes)
CITY_DICT = {label: coord for (label, coord) in zip(CITY_LABELS, CITY_COORD)}

# Population initialization function
def init(pop_size):
    def random_permutation():
        population = list()
        for _ in range(pop_size):
            # Each individual is a random permutation of the set of cities
            individual = list(numpy.random.permutation(CITY_LABELS))
            population.append(individual)
        return population
    
    return random_permutation()


#fitness function
# Calculates the fitness of all individuals in the population

def fit(population):
    fitness = list()
    for individual in population:
        distance = 0
        for i, city in enumerate(individual):
            s = CITY_DICT[individual[i-1]]
            t = CITY_DICT[individual[i]]
            distance += numpy.linalg.norm(s-t)
        fitness.append(1/distance)
    return fitness

# Selection function
def selection(population, fitness, n):
    def roulette():
        # Obtaining the indices for each individual in the population
        idx = numpy.arange(0, len(population))
        # Calculation of selection probabilities based on individuals' aptitude
        probabilities = fitness/numpy.sum(fitness)
        # Choice of parent indexes
        parents_idx = numpy.random.choice(idx, size=n, p=probabilities)
        # Choice of parents based on selected indexes
        parents = numpy.take(population, parents_idx, axis=0)
        parents = [(parents[i], parents[i+1])
                   for i in range(0, len(parents)-1, 2)]
        return parents
    return roulette()

# Crossover function
def crossover(parents, crossover_rate=0.9):
    def ordered():
        children = list()
        # Iteration by all pairs of parents
        for pair in parents:
            if numpy.random.random() < crossover_rate:
                for (parent1, parent2) in [(pair[0], pair[1]), (pair[1], pair[0])]:
                    # Cut segment definition
                    points = numpy.random.randint(0, len(parent1), 2)
                    start = min(points)
                    end = max(points)
                    segment1 = [x for x in parent1[start:end]]
                    segment2 = [x for x in parent2[end:] if x not in segment1]
                    segment3 = [x for x in parent2[:end] if x not in segment1]
                    child = segment3 + segment1 + segment2
                    children.append(child)
            else:
                # If the crossing does not occur, the parents remain in the next generation
                children.append(pair[0])
                children.append(pair[1])
        return children
    return ordered()


#mutation function
def mutation(children, mutation_rate=0.05):
    def swap():
        for i, child in enumerate(children):
            if numpy.random.random() < mutation_rate:
                [a, b] = numpy.random.randint(0, len(child), 2)
                children[i][a], children[i][b] = children[i][b], children[i][a]
        return children
    return swap()


# Stop criterion function
def stop():
    return False

# Elitism function
def elitism(population, fitness, n):
    # Select n most suitable individuals
    return [e[0] for e in sorted(zip(population, fitness),
                                 key=lambda x:x[1], reverse=True)[:n]]


def base_algorithm(pop_size, max_generations, elite_size=0):
    population = init(pop_size)
    yield 0, population, fit(population)
    for g in range(max_generations):
        fitness = fit(population)
        elite = elitism(population, fitness, elite_size)
        parents = selection(population, fitness, pop_size - elite_size)
        children = crossover(parents)
        children = mutation(children)
        population = elite + children
        yield g+1, population, fit(population)
        #if stop():
            #break

# Animation  Function

def ga():
    run = base_algorithm(pop_size=100, max_generations=300, elite_size=10)
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(2, 3, wspace=0.45, hspace=0.35)

    ax3 = fig.add_subplot(gs[0, 0])
    ax3.set_xlabel('x (kms)')
    ax3.set_ylabel('y (kms)')
    ax3.set_title('Cities', fontweight='bold', pad=10)
    ax3.set_xlim([-400, 410])
    ax3.set_ylim([-400, 410])
    ax3.scatter(CITY_COORD[:, 0],CITY_COORD[:, 1], c='r', edgecolors='black', alpha=0.85)
    

    x = []
    y_min = []
    y_mean = []

    ax0 = fig.add_subplot(gs[1, 0])
    

    ax1 = fig.add_subplot(gs[:, 1:])
  

    def animate(args):
        ax0.clear()
        ax1.clear()
        ax0.set_title('Best path distance in every generation', fontweight='bold', pad=10)
        ax0.set_xlabel('Generations')
        ax0.set_ylabel('Distance (kms)')
        g, population, fitness = args
        x.append(g)
        dist = [1/f for f in fitness]
        y_min.append(numpy.min(dist))
        y_mean.append(numpy.mean(dist))
        ax0.plot(x, y_min, color='blue', alpha=0.7, label='Fittest individual')
        #ax0.plot(x, y_mean, color='blue', alpha=0.7, label='Média da população')
        ax0.legend(loc='upper right')
        #ax1.set_title('Fittest individual')
        ax1.set_title(f"Best Path Cost : {numpy.min(dist)} kms")
        ax1.set_xlabel('x (kms)')
        ax1.set_ylabel('y (kms)')
        ax1.set_xlim([-400, 410])
        ax1.set_ylim([-400, 410])
        ax1.scatter(CITY_COORD[:, 0],
                    CITY_COORD[:, 1], c='r', edgecolors='black', alpha=0.85)
        solution = max(zip(population, fitness), key=lambda x: x[1])[0]
        P = numpy.array([CITY_DICT[s]
                         for s in solution] + [CITY_DICT[solution[0]]])
        ax1.plot(P[:, 0], P[:, 1], '--',c='black', alpha=0.85)
        return


    try:

        #anim = matplotlib.animation.FuncAnimation(
        anim =FuncAnimation(
            fig, animate, frames=run, interval=50, repeat=False)
        anim.save(f'xyz.gif', writer='')

        #plt.tight_layout(pad=3.5)
        #plt.show()

    except AttributeError:

        pass
    
    #Ant colony Optimization
    
    class SolveTSPUsingACO:
    class Edge:
        def __init__(self, a, b, weight, initial_pheromone):
            self.a = a
            self.b = b
            self.weight = weight
            self.pheromone = initial_pheromone

    class Ant:
        def __init__(self, alpha, beta, num_nodes, edges):
            self.alpha = alpha
            self.beta = beta
            self.num_nodes = num_nodes
            self.edges = edges
            self.tour = None
            self.distance = 0.0
        def _select_node(self):
            roulette_wheel = 0.0
            unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour]
            heuristic_total = 0.0
            for unvisited_node in unvisited_nodes:
                heuristic_total += self.edges[self.tour[-1]][unvisited_node].weight
            for unvisited_node in unvisited_nodes:
                roulette_wheel += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
            random_value = random.uniform(0.0, roulette_wheel)
            wheel_position = 0.0
            for unvisited_node in unvisited_nodes:
                wheel_position += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
                if wheel_position >= random_value:
                    return unvisited_node

        def find_tour(self):
            self.tour = [random.randint(0, self.num_nodes - 1)]
            while len(self.tour) < self.num_nodes:
                self.tour.append(self._select_node())
            return self.tour

        def get_distance(self):
            self.distance = 0.0
            for i in range(self.num_nodes):
                self.distance += self.edges[self.tour[i]][self.tour[(i + 1) % self.num_nodes]].weight
            return self.distance
        def __init__(self, mode='ACS', colony_size=10, elitist_weight=1.0, min_scaling_factor=0.001, alpha=1.0, beta=3.0,
                 rho=0.1, pheromone_deposit_weight=1.0, initial_pheromone=1.0, steps=100, nodes=None, labels=None):
        self.mode = mode
        self.colony_size = colony_size
        self.elitist_weight = elitist_weight
        self.min_scaling_factor = min_scaling_factor
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        self.num_nodes = len(nodes)
        self.nodes = nodes
        self.tours=[]
        cities=self.nodes
        if labels is not None:
            self.labels = labels
        else:
            self.labels = range(1, self.num_nodes + 1)
        self.edges = [[None] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                self.edges[i][j] = self.edges[j][i] = self.Edge(i, j, math.sqrt(
                    pow(self.nodes[i][0] - self.nodes[j][0], 2.0) + pow(self.nodes[i][1] - self.nodes[j][1], 2.0)),
                                                                initial_pheromone)
        self.ants = [self.Ant(alpha, beta, self.num_nodes, self.edges) for _ in range(self.colony_size)]
        self.global_best_tour = None
        self.global_best_tours =[]
        self.global_best_distance = float("inf")

    
