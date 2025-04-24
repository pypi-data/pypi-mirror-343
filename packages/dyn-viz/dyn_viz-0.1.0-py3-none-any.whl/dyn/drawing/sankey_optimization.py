"""This module is used to optimize sankey diagram for better readability.

.. todo::
    * document rest of code (only new Facade currently is)
    * reorganize classes for better integration (useful to remove Facade next)

Optimize a sankey diagram.

.. code:: bash

    python sankey_optimization.py [-h] [--stats STATS]
        [--stop STOP] [-o OUT] [-a {GA,HA,SA}] sankey

    Positional arguments:
    * sankey                sankey file

    Options:
    * -h, --help            show this help message and exit
    * --stats STATS         name of a csv file which will be used to save the
                            algorithm statistics
    * --stop STOP           stop at this iteration
    * -o OUT, --out OUT     output directory
    * -a {GA,HA,SA}, --algorithm {GA,HA,SA}
                            optimization algorithm
"""  # noqa: E501
import argparse
import itertools
import logging
import math
import random
import time
from enum import Enum
from typing import Literal

import numpy as np
import pandas as pd
from dyn.core.community_graphs import EvolvingCommunitiesGraph
from dyn.core.files_io import load_graph, save_graph

__all__ = [
    "GeneticAlgorithm",
    "HybridGeneticAlgorithm",
    "SimulatedAnnealing",
    "SankeyOptimizer",
]


LOGGER = logging.getLogger(__name__)


class SwapOrder(Enum):
    FIRST_TO_LAST = 1
    LAST_TO_FIRST = 2
    RANDOM = 3


def calculate_cost(arr):
    """
    Calculate the cost of the matrix.

    The cost represent the number of crossing between the edges of the matrix,
    with the crossing between bigger edges having a larger cost.
    """
    sums = arr[-1:0:-1, 0:-1].cumsum(0)[::-1].cumsum(1)
    copy = arr[:-1, 1:]
    total = np.sum(sums * copy)
    return total


class RankFunction:
    def __init__(self):
        self.params = dict()

    def __call__(self, array, sp=1.5):
        if (
            self.params.get("number") != len(array)
            or self.params.get("sp") != sp
        ):
            self.params["number"] = len(array)
            self.params["sp"] = sp

            def f(pos):
                return 2 - sp + (2 * (sp - 1) * pos / (len(array) - 1))

            p = [f(i) for i in range(len(array))]
            p = [v / sum(p) for v in p]
            self.params["p"] = p
        return self.params["p"]


rank_function = RankFunction()


class Environment:
    def __init__(self, graph: EvolvingCommunitiesGraph):
        self.graph = graph
        self.arrays = []
        self.labels = []
        nodes = list(self.graph.nodes)
        for t1, t2 in zip(self.graph.snapshots[:-1], self.graph.snapshots[1:]):
            if len(self.labels) == 0:
                self.labels.append(
                    sorted(
                        [*self.graph.snapshot_nodes(t1)],
                        key=lambda n: nodes.index(n),
                    )
                )
            nodes_from = self.labels[-1]
            nodes_to = sorted(
                [*self.graph.snapshot_nodes(t2)], key=lambda n: nodes.index(n)
            )
            self.labels.append(nodes_to)
            array = pd.DataFrame(0, index=nodes_from, columns=nodes_to)
            for node_from in nodes_from:
                for node_to in self.graph.successors(node_from):
                    array.at[node_from, node_to] = self.graph.edges[
                        node_from, node_to
                    ]["flow"]
            self.arrays.append(array.values)

    @property
    def identity_genes(self):
        return [list(range(len(layer_labels))) for layer_labels in self.labels]

    def genes_as_labels(self, genes):
        lbls = []
        for i, g in enumerate(genes):
            lbl = self.labels[i][list(g)]
            lbls.append(lbl)
        return lbls

    def genes_as_arrays(self, genes):
        """Return the genes as a list of arrays representing the graph."""
        gs = [np.array(g, dtype=int) for g in genes]
        arrays = [
            arr[:, r2][r1] for arr, r1, r2 in zip(self.arrays, gs[:-1], gs[1:])
        ]
        return arrays

    def genes_as_graph(self, genes):
        res = EvolvingCommunitiesGraph(community="all")
        for nodes, gene in zip(self.labels, genes):
            ordered = [nodes[g] for g in gene]
            for order, node in enumerate(ordered):
                res.add_node(node, **self.graph.nodes[node])
        for n1, n2 in self.graph.edges:
            res.add_edge(n1, n2, **self.graph.edges[n1, n2])
        return res

    def cost(self, genes):
        arrays = self.genes_as_arrays(genes)
        return sum((calculate_cost(a) for a in arrays))

    def calculate_fitness(self, genes):
        return -self.cost(genes)

    def is_optimal(self, genes):
        return self.cost(genes) == 0

    def create_random_individual(self):
        lengths = [len(lbl) for lbl in self.labels]
        genes = [list(range(length)) for length in lengths]
        for g in genes:
            np.random.shuffle(g)
        return self.create_individual(genes=genes)

    def get_genes_to_modify(self, number):
        candidate_genes = [
            i for i, labels in enumerate(self.labels) if len(labels) > 1
        ]
        if len(candidate_genes) == 0:
            return []
        count = random.choice(range(1, min(number + 1, len(candidate_genes))))
        genes_id = random.sample(candidate_genes, count)
        # genes_id = [i for i in range(number) if random.random() < 0.8]
        return genes_id

    def create_individual(self, genes):
        return Individual(environment=self, genes=genes)


class Individual:
    def __init__(self, environment, genes):
        self.environment = environment
        self.genes = genes
        self._fitness = None

    @property
    def genes(self):
        return self._genes

    @genes.setter
    def genes(self, genes):
        self._genes = tuple([tuple(g) for g in genes])
        self._fitness = None

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = self.environment.calculate_fitness(self.genes)
        return self._fitness

    @property
    def is_optimal(self) -> bool:
        return self.environment.is_optimal(self.genes)

    def __eq__(self, other):
        return self.genes == other.genes

    def tweak(self):
        """
        Tweak the solution for the simulated annealing.

        Randomly choose a layer and swap two adjacent genes.
        """
        candidate_layers = self.environment.get_genes_to_modify(1)
        if len(candidate_layers) == 0:
            return self
        gene_id = candidate_layers[0]
        genes = [list(g) for g in self.genes]
        idx = random.choice(range(len(genes[gene_id]) - 1))
        g = genes[gene_id]
        g[idx], g[idx + 1] = g[idx + 1], g[idx]
        return self.environment.create_individual(genes=genes)

    def mutate(self, p=None):
        """Create a new individual with mutated genes.

        The mutation is randomly chosen from the available mutations.
        """
        choices_dict = {
            "swap": self.mutation_swap,
            "reversion": self.mutation_reversion,
            "random": self.mutation_random,
            "insertion": self.mutation_insertion,
        }
        if p is None:
            choices = list(choices_dict.values())
            f = random.choice(choices)
        else:
            choices, proba = [], []
            for k in p:
                proba.append(p[k])
                choices.append(choices_dict[k])
            f = np.random.choice(choices, p=proba)
        genes = [list(g) for g in self.genes]
        genes_to_modify = self.environment.get_genes_to_modify(len(self.genes))
        for i in genes_to_modify:
            genes[i] = f(genes[i])
        return self.environment.create_individual(genes=genes)

    def mutation_random(self, gene):
        """Create a new shuffled gene."""
        gene = list(gene)
        np.random.shuffle(gene)
        return gene

    def mutation_swap(self, gene):
        """Create a new gene using a swap mutation."""
        if len(gene) < 2:
            return gene
        gene = list(gene)
        # Randomly select two different indexes
        idx = random.sample(range(len(gene) + 1), 2)
        idx1, idx2 = sorted(idx)
        # Reverse the order of the genes between the two indexes
        part = gene[idx1:idx2]
        part.reverse()
        gene = gene[:idx1] + part + gene[idx2:]
        return gene

    def mutation_reversion(self, gene):
        """Create a new gene using a reversion mutation."""
        if len(gene) < 2:
            return gene
        gene = list(gene)
        # Randomly select two different indexes
        idx1, idx2 = random.sample(range(len(gene)), 2)
        # Swap the values at the two indexes
        gene[idx1], gene[idx2] = gene[idx2], gene[idx1]
        return gene

    def mutation_insertion(self, gene):
        """Create a new gene using an insertion mutation."""
        if len(gene) < 2:
            return gene
        gene = list(gene)
        # Randomly select two different indexes
        idx1, idx2 = random.sample(range(len(gene)), 2)
        # Move the element at the second index to the first index
        gene.insert(idx1, gene.pop(idx2))
        return gene

    def swap_2opt_all(self, count: int = None, order=SwapOrder.RANDOM):
        """Modify the individual using a 2-opt local search.

        A 2-opt local search is executed in each layer.
        For each layer, the best of `count` 2-opt reversions is kept.

        :param count: number of reversions executed
        :param order: order in which the layers are processed
        """
        best = [list(g) for g in self.genes]
        best_fitness = self.fitness
        idxs = list(range(len(self.genes)))
        if order == SwapOrder.LAST_TO_FIRST:
            idxs = idxs[::-1]
        elif order == SwapOrder.RANDOM:
            np.random.shuffle(idxs)
        for i in idxs:
            gene = self.genes[i]
            tmp = [list(g) for g in best]
            swap_idxs = list(itertools.combinations(range(len(gene)), 2))
            if count is not None and count < len(swap_idxs):
                swap_idxs = random.sample(swap_idxs, count)
            for idx1, idx2 in swap_idxs:
                g = list(self.genes[i])
                g[idx1], g[idx2] = g[idx2], g[idx1]
                tmp[i] = g
                fitness = self.environment.calculate_fitness(tmp)
                if fitness > best_fitness:
                    best[i] = g
                    best_fitness = fitness
        if best_fitness > self.fitness:
            self.genes = best
            self._fitness = best_fitness


class GeneticAlgorithm:
    def __init__(
        self,
        environment,
        population=None,
        crossover_rate=0.7,
        mutation_rate=0.2,
        crossover_p=None,
        mutation_p=None,
    ):
        self.environment = environment
        self.population = [] if population is None else population
        self.pop_size = len(self.population)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.crossover_p = crossover_p
        self.mutation_p = mutation_p
        self.iteration = 0
        self.total_time = 0

    def create_random_population(self, size):
        return [
            self.environment.create_random_individual() for _ in range(size)
        ]

    def init_random_population(self, size):
        population = self.create_random_population(size)
        self.population = population
        self.pop_size = size

    def replace_duplicate_individuals(self):
        """Replace duplicate individuals by random individuals."""
        new_pop = []
        for indiv in self.population:
            if indiv not in new_pop:
                new_pop.append(indiv)
        size_missing = self.pop_size - len(new_pop)
        random_pop = self.create_random_population(size_missing)
        self.population = new_pop + random_pop

    def select_tournament(self, size: int = 2):
        """
        Organize a tournament selection to obtain an individual in the
        population.

        :param size:
            size of the random subpopulation amongst which the
            most fit individual will be selected
        """
        individuals = random.sample(self.population, size)
        return max(individuals, key=lambda i: i.fitness)

    def select_rank_roulette(self, count: int = None, replace: bool = True):
        """Select individuals using a rank roulette.

        :param count: number of individuals to return
        :param replace: can return several times the same individual
        """
        # Sort worse first
        pop = sorted(self.population, key=lambda i: i.fitness)
        p = rank_function(pop, sp=1.8)
        return np.random.choice(pop, size=count, p=p, replace=replace)

    def select_individuals(self, count=2):
        return self.select_rank_roulette(count=count)

    def crossover_random(self, indiv1, indiv2, p=None):
        """Randomly apply a crossover method for the two individuals."""
        choices_dict = {
            "ordered": self.crossover_ordered,
            "cycle": self.crossover_cycle,
            "layer": self.crossover_layer,
        }
        if p is None:
            choices = list(choices_dict.values())
            f = random.choice(choices)
        else:
            choices, proba = [], []
            for k in p:
                proba.append(p[k])
                choices.append(choices_dict[k])
            f = np.random.choice(choices, p=proba)
        return f(indiv1, indiv2)

    def crossover_layer(self, indiv1, indiv2):
        """Randomly choose layers from the first or the second individual."""
        assert len(indiv1.genes) == len(
            indiv2.genes
        ), "The two individuals must have the same genes length"
        genes1, genes2 = [], []
        genes_to_modify = self.environment.get_genes_to_modify(
            len(indiv1.genes)
        )
        for i, (gene1, gene2) in enumerate(zip(indiv1.genes, indiv2.genes)):
            assert len(gene1) == len(gene2)
            if i not in genes_to_modify:
                genes1.append(np.copy(gene2))
                genes2.append(np.copy(gene1))
            else:
                genes1.append(np.copy(gene1))
                genes2.append(np.copy(gene2))
        return (
            self.environment.create_individual(genes=genes1),
            self.environment.create_individual(genes=genes2),
        )

    def crossover_ordered(self, indiv1, indiv2):
        """Return two children using an ordered crossover."""
        assert len(indiv1.genes) == len(
            indiv2.genes
        ), "The two individuals must have the same genes length"
        genes1, genes2 = [], []
        genes_to_modify = self.environment.get_genes_to_modify(
            len(indiv1.genes)
        )
        for i, (gene1, gene2) in enumerate(zip(indiv1.genes, indiv2.genes)):
            assert len(gene1) == len(gene2)
            if i not in genes_to_modify:
                genes1.append(np.copy(gene1))
                genes2.append(np.copy(gene2))
                continue
            idx = random.sample(range(len(gene1)), 2)
            idx1, idx2 = np.sort(idx)
            og1 = np.array(gene1)[~np.isin(gene1, gene2[idx1:idx2])]
            og2 = np.array(gene2)[~np.isin(gene2, gene1[idx1:idx2])]
            g1 = np.concatenate((og1[:idx1], gene2[idx1:idx2], og1[idx1:]))
            g2 = np.concatenate((og2[:idx1], gene1[idx1:idx2], og2[idx1:]))
            genes1.append(g1.tolist())
            genes2.append(g2.tolist())
        return (
            self.environment.create_individual(genes=genes1),
            self.environment.create_individual(genes=genes2),
        )

    def crossover_cycle(self, indiv1, indiv2):
        """Return two children using a cycle crossover."""
        assert len(indiv1.genes) == len(
            indiv2.genes
        ), "The two individuals must have the same genes length"
        genes1, genes2 = [], []
        genes_to_modify = self.environment.get_genes_to_modify(
            len(indiv1.genes)
        )
        for i, (gene1, gene2) in enumerate(zip(indiv1.genes, indiv2.genes)):
            assert len(gene1) == len(gene2)
            if i not in genes_to_modify:
                genes1.append(np.copy(gene1))
                genes2.append(np.copy(gene2))
                continue
            cycle_masks = []
            start_idx = 0
            or_mask = np.zeros(len(gene1), dtype=bool)
            while not np.all(or_mask):
                mask = np.zeros(len(gene1), dtype=bool)
                mask[start_idx] = True
                or_mask[start_idx] = True
                idx = start_idx
                while gene2[idx] != gene1[start_idx]:
                    idx = list(gene1).index(gene2[idx])
                    mask[idx] = True
                    or_mask[idx] = True
                cycle_masks.append(mask)
                try:
                    start_idx = or_mask.tolist().index(False)
                except ValueError:
                    break
            mask_even = np.any(cycle_masks[1::2], axis=0)
            g1 = np.copy(gene1)
            g1[mask_even] = np.array(gene2)[mask_even]
            genes1.append(g1.tolist())
            g2 = np.copy(gene2)
            g2[mask_even] = np.array(gene1)[mask_even]
            genes2.append(g2.tolist())
        return (
            self.environment.create_individual(genes=genes1),
            self.environment.create_individual(genes=genes2),
        )

    def iterate(self):
        """Execute an iteration of the algorithm."""
        assert self.crossover_rate + self.mutation_rate <= 1
        self.iteration += 1

        # Select new population
        parents_pop_count = int(
            self.pop_size * (1 - self.crossover_rate - self.mutation_rate)
        )
        pop = sorted(self.population, key=lambda i: i.fitness, reverse=True)
        new_pop = pop[:parents_pop_count]

        # Create children using parents crossover
        children = []
        count = int(self.crossover_rate * self.pop_size)
        count = count + 1 if count % 2 != 0 else count
        parents = self.select_individuals(count=count)
        for i in range(0, len(parents), 2):
            ind1, ind2 = parents[i], parents[i + 1]
            new_children = self.crossover_random(ind1, ind2, self.crossover_p)
            children.extend(new_children)
        new_pop.extend(children)

        # Create mutated individuals from parents
        count = int(self.mutation_rate * self.pop_size)
        count = count + 1 if count % 2 != 0 else count
        to_mutate = self.select_individuals(count=count)
        mutated = [ind.mutate(self.mutation_p) for ind in to_mutate]
        new_pop.extend(mutated)

        self.population = new_pop

    def iterator(self, stop=None):
        while True:
            start = time.time()
            self.iterate()
            self.replace_duplicate_individuals()
            self.total_time += time.time() - start
            if stop is not None and self.iteration > stop:
                return
            yield self.iteration

    def get_best_individual(self):
        """Return the best individual in the population."""
        return max(self.population, key=lambda i: i.fitness)


class HybridGeneticAlgorithm(GeneticAlgorithm):
    def init_random_population(self, size):
        """Create the population and do local search on half of the
        population.
        """
        population = self.create_random_population(size)
        self.population = population
        self.pop_size = size
        for i in range(int(self.pop_size / 2)):
            self.population[i].swap_2opt_all(count=100)

    def iterator(self, stop=None):
        while True:
            start = time.time()
            self.iterate()
            self.replace_duplicate_individuals()
            self.local_search()
            self.total_time += time.time() - start
            if stop is not None and self.iteration > stop:
                return
            yield self.iteration

    def local_search(self, swap_count: int = 10):
        """
        Do a local search for each individual of the population.

        :param swap_count:
            number of swap for each of the 2-opt optimization
        """
        for ind in self.population:
            ind.swap_2opt_all(count=swap_count, order=SwapOrder.RANDOM)

    def post_local_search(self, count: int = 10, swap_count: int = 2000):
        """
        Do a local search to try to optimize the final result.

        Optimize the best individual using a 2-opt swap.

        :param count: number of times the local search will be executed
        :param swap_count: number of swap for each of the 2-opt optimization
        """
        start = time.time()
        for i in range(count):
            best = self.get_best_individual()
            best.swap_2opt_all(count=swap_count, order=SwapOrder.RANDOM)
        self.total_time += time.time() - start


class SimulatedAnnealing:
    def __init__(self, solution, temp_0, temp_end=1, cooling="exponential"):
        self.temp_0 = temp_0
        self.temp_end = temp_end
        self.cooling = cooling
        self.temperature = self.temp_0
        self.solution = solution
        self.best = self.solution
        self.iteration = 0
        self.total_time = 0

    def iterate(self, alpha, steps=1):
        """Iterate one step of the simulated annealing."""
        self.iteration += 1

        new_sol = self.solution.tweak()
        chance = math.exp(
            (new_sol.fitness - self.solution.fitness) / self.temperature
        )

        if new_sol.fitness > self.solution.fitness or random.random() < chance:
            self.solution = new_sol

        if self.iteration % steps == 0:
            if self.cooling == "exponential":
                self.temperature = self.temp_0 * alpha**self.iteration
            elif self.cooling == "logarithmical":
                self.temperature = self.temp_0 / (
                    1 + alpha * math.log10(1 + self.iteration)
                )
            elif self.cooling == "linear":
                self.temperature = self.temp_0 / (1 + alpha * self.iteration)
            elif self.cooling == "quadratic":
                self.temperature = self.temp_0 / (
                    1 + alpha * self.iteration**2
                )
            else:
                raise ValueError("Unknown cooling schedule type.")

        if self.solution.fitness > self.best.fitness:
            self.best = self.solution

    def iterator(self, alpha, steps=1, iterations=None):
        """Start the simulated annealing algorithm."""
        while True:
            start = time.time()
            self.iterate(alpha=alpha, steps=steps)
            self.total_time += time.time() - start
            if iterations is not None and self.iteration > iterations:
                return
            elif self.temperature <= self.temp_end:
                return
            yield self.iteration


def start_algorithm(sankey_file, stop, out_file=None, size=80, algo_params={}):
    time_start = time.time()
    graph = EvolvingCommunitiesGraph.from_graph(load_graph(sankey_file))
    env = Environment(graph=graph)
    algo = GeneticAlgorithm(environment=env, **algo_params)
    algo.init_random_population(size=size)
    stats_history = []
    fitness = pd.DataFrame([i.fitness for i in algo.population])
    fitness_stats = fitness.describe()
    stats_history.append(fitness_stats[0].to_dict())
    history_period = 10
    for iteration in algo.iterator(stop=stop):
        if iteration % history_period == 0:
            fitness = pd.DataFrame([i.fitness for i in algo.population])
            fitness_stats = fitness.describe()
            stats_history.append(fitness_stats[0].to_dict())
    time_end = time.time()
    best = algo.get_best_individual()
    LOGGER.debug(
        "Best: {:.10g} in {:.2f} seconds."
        "".format(env.cost(best.genes), algo.total_time)
    )
    if out_file is not None:
        save_graph(
            env.genes_as_graph(best.genes),
            out_file,
        )
    out = {
        "iteration": algo.iteration,
        "total_time": algo.total_time,
        "best": {
            "cost": env.cost(best.genes),
            "arrays": [a.tolist() for a in env.genes_as_arrays(best.genes)],
            "labels": [g.tolist() for g in env.genes_as_labels(best.genes)],
        },
        "history": {"period": history_period, "stats": stats_history},
        "start_time": time_start,
        "end_time": time_end,
    }
    return out


def start_hybrid_algorithm(
    sankey_file, stop, out_file=None, size=80, algo_params={}
):
    time_start = time.time()
    graph = EvolvingCommunitiesGraph.from_graph(load_graph(sankey_file))
    env = Environment(graph=graph)
    algo = HybridGeneticAlgorithm(environment=env, **algo_params)
    algo.init_random_population(size=size)
    stats_history = []
    fitness = pd.DataFrame([i.fitness for i in algo.population])
    fitness_stats = fitness.describe()
    stats_history.append(fitness_stats[0].to_dict())
    history_period = 1
    for iteration in algo.iterator(stop=stop):
        if iteration % history_period == 0:
            fitness = pd.DataFrame([i.fitness for i in algo.population])
            fitness_stats = fitness.describe()
            stats_history.append(fitness_stats[0].to_dict())
    algo.post_local_search()
    time_end = time.time()
    best = algo.get_best_individual()
    LOGGER.debug(
        "Best: {:.10g} in {:.2f} seconds."
        "".format(env.cost(best.genes), algo.total_time)
    )
    if out_file is not None:
        save_graph(
            env.genes_as_graph(best.genes),
            out_file,
        )
    out = {
        "iteration": algo.iteration,
        "total_time": algo.total_time,
        "best": {
            "cost": env.cost(best.genes),
            "arrays": [a.tolist() for a in env.genes_as_arrays(best.genes)],
            "labels": [g.tolist() for g in env.genes_as_labels(best.genes)],
        },
        "history": {"period": history_period, "stats": stats_history},
        "start_time": time_start,
        "end_time": time_end,
    }
    return out


def start_simulated_annealing(
    sankey_file, out_file=None, iterations=None, algo_params={}
):
    time_start = time.time()
    graph = EvolvingCommunitiesGraph.from_graph(load_graph(sankey_file))
    env = Environment(graph=graph)
    solution = env.create_random_individual()
    alpha = algo_params.pop("alpha")
    steps = algo_params.pop("steps", 1)
    algo = SimulatedAnnealing(solution=solution, **algo_params)
    best_history = [algo.best.fitness]
    solution_history = [algo.solution.fitness]
    temperature_history = [algo.temperature]
    history_period = 1000
    for iteration in algo.iterator(alpha, steps=steps, iterations=iterations):
        if iteration % history_period == 0:
            best_history.append(algo.best.fitness)
            solution_history.append(algo.solution.fitness)
            temperature_history.append(algo.temperature)
    time_end = time.time()
    best_genes = algo.best.genes
    LOGGER.debug(
        "Best: {:.10g} in {:.2f} seconds. Final temperature: {:.4f}"
        "".format(env.cost(best_genes), algo.total_time, algo.temperature)
    )

    if out_file is not None:
        save_graph(
            env.genes_as_graph(best.genes),
            out_file,
        )

    out = {
        "iteration": algo.iteration,
        "total_time": algo.total_time,
        "best": {
            "cost": env.cost(best_genes),
            "arrays": [a.tolist() for a in env.genes_as_arrays(best_genes)],
            "labels": [g.tolist() for g in env.genes_as_labels(best_genes)],
        },
        "history": {
            "period": history_period,
            "best": best_history,
            "solution": solution_history,
            "temperature": temperature_history,
        },
        "start_time": time_start,
        "end_time": time_end,
    }
    return out


class SankeyOptimizer:
    """This class is a Facade for the different Sankey optimizers.

    :param graph: community flow graph
    :param algo: chosen optimizer type
    :param time_max: maximum time allocated to optimization process
    :param optimizer_kwargs:
        keyworded arguments passed to optimizer constructor
    """

    def __init__(
        self,
        graph: EvolvingCommunitiesGraph,
        algo: Literal["SA", "GA", "HA"] = "SA",
        time_max: float = 30,
        **optimizer_kwargs,
    ) -> None:
        self.graph = graph
        self.environment = Environment(graph=self.graph)
        self.time_max = time_max
        self.optimizer = self.init_optimizer(algo=algo, **optimizer_kwargs)

    def init_optimizer(self, algo: Literal["SA", "GA", "HA"], **kwargs):
        """Create and initialize actual sankey optimizer.

        :param algo: chosen algorithm
        :param kwargs: parameters passed to actual sankey optimizer
        """
        if algo == "GA":
            optimizer = GeneticAlgorithm(
                environment=self.environment, **kwargs
            )
            optimizer.init_random_population(size=100)
            return optimizer
        if algo == "SA":
            solution = self.environment.create_random_individual()
            return SimulatedAnnealing(solution, 1000, 0)
        if algo == "HA":
            optimizer = HybridGeneticAlgorithm(
                environment=self.environment, **kwargs
            )
            optimizer.init_random_population(size=100)
            return optimizer
        raise ValueError(
            f"unknown optimizer type: {algo} (must be among 'GA', 'SA', 'HA')"
        )

    def run(self) -> EvolvingCommunitiesGraph:
        """Run sankey optimization.

        :return: optimized community flow graph
        """

        best = Individual(self.environment, self.environment.identity_genes)
        if best.is_optimal:
            LOGGER.debug("initial solution already optimal")
            return self.environment.genes_as_graph(best.genes)
        args = {}
        debug_steps = 1
        match self.optimizer:
            case SimulatedAnnealing():
                args = {"alpha": 0.999987}
                debug_steps = 1000
            case _:
                pass
        t0 = time.time()
        for iteration in self.optimizer.iterator(**args):
            match self.optimizer:
                case SimulatedAnnealing():
                    best = self.optimizer.best
                case _:
                    best = self.optimizer.get_best_individual()
            if iteration % debug_steps == 0:
                LOGGER.debug(self.state_string)
            if time.time() >= t0 + self.time_max or best.is_optimal:
                optimal_msg = " (optimal)" if best.is_optimal else ""
                LOGGER.debug(
                    "final: best cost "
                    f"{self.environment.cost(best.genes):.10g}{optimal_msg}"
                )
                return self.environment.genes_as_graph(best.genes)

    @property
    def state_string(self) -> str:
        """Optimizer state expressed for logger/print"""
        match self.optimizer:
            case SimulatedAnnealing():
                return (
                    "iteration {:04d}: cost {:.10g}, current: {:.10g}, "
                    "temperature: {:.4f}, time: {:.4f}"
                    "".format(
                        self.optimizer.iteration,
                        -self.optimizer.best.fitness,
                        -self.optimizer.solution.fitness,
                        self.optimizer.temperature,
                        self.optimizer.total_time,
                    )
                )
            case _:
                return (
                    "iteration {:04d}: cost {:.10g}, time: {:.4f}"
                    "".format(
                        self.optimizer.iteration,
                        self.environment.cost(
                            self.optimizer.get_best_individual().genes
                        ),
                        self.optimizer.total_time,
                    )
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute a metaheuristic algorithm for optimizing "
        "sankey diagrams"
    )
    parser.add_argument(
        "--stats",
        help="name of a csv file which will be used to save "
        "the algorithm statistics",
    )
    parser.add_argument("--stop", type=int, help="stop at this iteration")
    parser.add_argument(
        "-o", "--out", type=str, default=None, help="output directory"
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        type=str,
        default="SA",
        choices=["GA", "HA", "SA"],
        help="optimization algorithm",
    )
    parser.add_argument("sankey", help="sankey file")
    args = parser.parse_args()

    out_filename = args.sankey if args.out is None else args.out

    graph = EvolvingCommunitiesGraph.from_graph(load_graph(args.sankey))

    env = Environment(graph=graph)
    best = Individual(env, env.identity_genes)

    history = []
    try:
        if best.is_optimal:
            LOGGER.debug("initial solution already optimal")
        elif args.algorithm == "GA":
            algo = GeneticAlgorithm(environment=env)
            algo.init_random_population(size=100)
            for iteration in algo.iterator(stop=args.stop):
                best = algo.get_best_individual()
                history.append(env.cost(best.genes))
                LOGGER.debug(
                    "iteration {:04d}: cost {:.10g}, time: {:.4f}"
                    "".format(
                        algo.iteration, env.cost(best.genes), algo.total_time
                    )
                )
                if best.is_optimal:
                    break
        elif args.algorithm == "HA":
            algo = HybridGeneticAlgorithm(environment=env)
            algo.init_random_population(size=100)
            for iteration in algo.iterator(stop=args.stop):
                best = algo.get_best_individual()
                history.append(env.cost(best.genes))
                LOGGER.debug(
                    "iteration {:04d}: cost {:.10g}, time: {:.4f}"
                    "".format(
                        algo.iteration, env.cost(best.genes), algo.total_time
                    )
                )
                if best.is_optimal:
                    break
        elif args.algorithm == "SA":
            solution = env.create_random_individual()
            algo = SimulatedAnnealing(solution, 1000, 0)
            for iteration in algo.iterator(0.999987, iterations=args.stop):
                best = algo.best
                history.append(-best.fitness)
                if iteration % 1000 == 0:
                    LOGGER.debug(
                        "iteration {:04d}: cost {:.10g}, current: {:.10g}, "
                        "temperature: {:.4f}, time: {:.4f}"
                        "".format(
                            algo.iteration,
                            -algo.best.fitness,
                            -algo.solution.fitness,
                            algo.temperature,
                            algo.total_time,
                        )
                    )
                if best.is_optimal:
                    break

        # for i in range(10):
        # population.append((algo.best, algo.solution))
        # print('post-optimisation {:04d}: cost {:.10g}'.format(i, env.cost(algo.best.genes)))  # noqa: E501
        # algo.best.swap_2opt_all(count=2000, order=SwapOrder.RANDOM)

        LOGGER.info("final: best cost {:.10g}".format(env.cost(best.genes)))
        save_graph(
            env.genes_as_graph(best.genes),
            args.out,
        )
    except KeyboardInterrupt:
        # import ipdb; ipdb.set_trace()
        LOGGER.info("final: best cost {:.10g}".format(env.cost(best.genes)))
        save_graph(
            env.genes_as_graph(best.genes),
            args.out,
        )

    # Display the best individual at each iteration
    import matplotlib.pyplot as plt

    x, y = [], []
    for i, value in enumerate(history):
        x.append(i)
        y.append(value)
    plt.plot(x, y, "b-")
    plt.xlim(xmin=-1, xmax=max(x) + 1)
    plt.xlabel("iteration")
    plt.ylabel("objective value")
    plt.show()
