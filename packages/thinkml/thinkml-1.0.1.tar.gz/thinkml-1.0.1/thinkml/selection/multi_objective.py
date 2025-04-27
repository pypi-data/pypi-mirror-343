"""
Multi-objective optimization techniques for ThinkML.
"""

import numpy as np
from sklearn.base import BaseEstimator
from scipy.optimize import minimize
from scipy.stats import norm

class MultiObjectiveOptimizer:
    """Multi-objective optimization using NSGA-II algorithm."""
    
    def __init__(self, param_space, objectives, n_iter=50,
                 population_size=100, random_state=None):
        """
        Initialize multi-objective optimizer.
        
        Parameters:
        -----------
        param_space : dict
            Dictionary with parameter names as keys and (low, high) tuples as values
        objectives : list of callable
            List of objective functions to optimize
        n_iter : int, default=50
            Number of iterations
        population_size : int, default=100
            Size of the population
        random_state : int or None, default=None
            Random state for reproducibility
        """
        self.param_space = param_space
        self.objectives = objectives
        self.n_iter = n_iter
        self.population_size = population_size
        self.random_state = random_state
        
        self.rng = np.random.RandomState(random_state)
        self.population = []
        self.fitness = []
        self.pareto_front = None
        self.pareto_set = None
        
    def _sample_random_point(self):
        """Sample random point from parameter space."""
        point = {}
        for param, (low, high) in self.param_space.items():
            point[param] = self.rng.uniform(low, high)
        return point
        
    def _evaluate_objectives(self, params):
        """Evaluate all objectives for given parameters."""
        return [obj(**params) for obj in self.objectives]
        
    def _dominates(self, a, b):
        """Check if solution a dominates solution b."""
        return (all(a_val >= b_val for a_val, b_val in zip(a, b)) and
                any(a_val > b_val for a_val, b_val in zip(a, b)))
                
    def _fast_non_dominated_sort(self, fitness):
        """Perform fast non-dominated sorting."""
        n_points = len(fitness)
        domination_count = np.zeros(n_points)
        dominated_solutions = [[] for _ in range(n_points)]
        fronts = [[]]
        
        for i in range(n_points):
            for j in range(i + 1, n_points):
                if self._dominates(fitness[i], fitness[j]):
                    dominated_solutions[i].append(j)
                    domination_count[j] += 1
                elif self._dominates(fitness[j], fitness[i]):
                    dominated_solutions[j].append(i)
                    domination_count[i] += 1
                    
            if domination_count[i] == 0:
                fronts[0].append(i)
                
        i = 0
        while fronts[i]:
            next_front = []
            for solution_idx in fronts[i]:
                for dominated_idx in dominated_solutions[solution_idx]:
                    domination_count[dominated_idx] -= 1
                    if domination_count[dominated_idx] == 0:
                        next_front.append(dominated_idx)
            i += 1
            if next_front:
                fronts.append(next_front)
                
        return fronts
        
    def _crowding_distance(self, fitness, front):
        """Calculate crowding distance for solutions in a front."""
        n_points = len(front)
        n_objectives = len(fitness[0])
        distances = np.zeros(n_points)
        
        for m in range(n_objectives):
            # Get the objective values for the front
            values = [fitness[i][m] for i in front]
            
            # Sort points by objective value
            sorted_idx = np.argsort(values)
            
            # Set boundary points to infinity
            distances[sorted_idx[0]] = np.inf
            distances[sorted_idx[-1]] = np.inf
            
            # Calculate crowding distance for intermediate points
            scale = values[sorted_idx[-1]] - values[sorted_idx[0]]
            if scale == 0:
                continue
                
            for i in range(1, n_points - 1):
                distances[sorted_idx[i]] += (
                    (values[sorted_idx[i + 1]] - values[sorted_idx[i - 1]]) / scale
                )
                
        return distances
        
    def optimize(self):
        """Run multi-objective optimization."""
        # Initialize population
        self.population = [
            self._sample_random_point()
            for _ in range(self.population_size)
        ]
        
        # Main optimization loop
        for _ in range(self.n_iter):
            # Evaluate objectives for current population
            self.fitness = [
                self._evaluate_objectives(params)
                for params in self.population
            ]
            
            # Non-dominated sorting
            fronts = self._fast_non_dominated_sort(self.fitness)
            
            # Create new population
            new_population = []
            new_fitness = []
            
            for front in fronts:
                if len(new_population) + len(front) > self.population_size:
                    # Calculate crowding distance
                    distances = self._crowding_distance(self.fitness, front)
                    
                    # Sort front by crowding distance
                    sorted_idx = np.argsort(-distances)
                    
                    # Add solutions until population is full
                    remaining = self.population_size - len(new_population)
                    for idx in sorted_idx[:remaining]:
                        new_population.append(self.population[front[idx]])
                        new_fitness.append(self.fitness[front[idx]])
                    break
                else:
                    # Add entire front
                    for idx in front:
                        new_population.append(self.population[idx])
                        new_fitness.append(self.fitness[idx])
                        
            # Update population and fitness
            self.population = new_population
            self.fitness = new_fitness
            
            # Create offspring through crossover and mutation
            offspring = self._create_offspring()
            
            # Add offspring to population
            self.population.extend(offspring)
            
        # Get final Pareto front
        final_fitness = [
            self._evaluate_objectives(params)
            for params in self.population
        ]
        fronts = self._fast_non_dominated_sort(final_fitness)
        
        # Store Pareto front and set
        pareto_idx = fronts[0]
        self.pareto_front = [final_fitness[i] for i in pareto_idx]
        self.pareto_set = [self.population[i] for i in pareto_idx]
        
        return self
        
    def _create_offspring(self):
        """Create offspring through crossover and mutation."""
        offspring = []
        
        while len(offspring) < self.population_size:
            # Select parents using tournament selection
            parent1 = self._tournament_select()
            parent2 = self._tournament_select()
            
            # Perform crossover
            child = self._crossover(parent1, parent2)
            
            # Perform mutation
            child = self._mutate(child)
            
            offspring.append(child)
            
        return offspring
        
    def _tournament_select(self, tournament_size=2):
        """Select parent using tournament selection."""
        tournament = self.rng.choice(
            len(self.population),
            size=tournament_size,
            replace=False
        )
        
        winner = tournament[0]
        for idx in tournament[1:]:
            if self._dominates(self.fitness[idx], self.fitness[winner]):
                winner = idx
                
        return self.population[winner]
        
    def _crossover(self, parent1, parent2):
        """Perform crossover between parents."""
        child = {}
        for param in self.param_space:
            if self.rng.random() < 0.5:
                child[param] = parent1[param]
            else:
                child[param] = parent2[param]
        return child
        
    def _mutate(self, individual):
        """Perform mutation on individual."""
        mutated = individual.copy()
        for param, (low, high) in self.param_space.items():
            if self.rng.random() < 0.1:  # mutation probability
                mutated[param] = self.rng.uniform(low, high)
        return mutated 