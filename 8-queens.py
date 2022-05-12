#!/usr/bin/env python3
"""8 queens homework. Two implementations, simulated annealing and genetic algorithm."""
__author__= "Benjamin Caulfield"

import random
import math
import sys

def main():
    games = int(sys.argv[1])
    annealing_wins = 0
    annealing_iters = 0
    genetic_wins = 0
    genetic_iters = 0
    for game in range(games):
        annealing_result = simulated_annealing()
        annealing_wins += annealing_result[0]
        annealing_iters += annealing_result[1]
        genetic_result = genetic_algorithm()
        genetic_wins += genetic_result[0]
        genetic_iters += genetic_result[1]
    print(games, "puzzles.")
    print(f"Simulated Annealing: {int(annealing_wins/games * 100)} % solved, average search cost: {int(annealing_iters / games)};")
    print(f"Genetic Algorithm: {int(genetic_wins/games * 100)} % solved, average search cost: {int(genetic_iters / games)};")
   

def simulated_annealing():
    board = create_board()
    t = 1
    while t < 2500:
        if heuristic(board) == 0:
            return (1, t)
        else:
            board = annealing_loop(board, t)
            t += 1
    return (0, t)

def annealing_loop(board, t):
    T = temperature(t)
    new_board = random_successor(board)
    delta = delta_e(board, new_board)
    if delta < 0:
        return new_board
    
    random_prob = random.random()
    new_board_prob = probability_function(delta, T)
    if new_board_prob > random_prob:
        return new_board
    return board  

def genetic_algorithm():
    pop = create_population()
    t = 1
    while t < 2500:
        if check_for_goal_state(pop):
            return (1, t)
        else:   
            selection = natural_selection(pop)
            ritual = mating_ritual(selection)
            pop = create_new_population(ritual)
            t += 1
    return (0, t)

def create_board():
    a = [0, 1, 2, 3, 4, 5, 6, 7]
    b = random.choices(a, k = 8)
    board = []
    for i in range(8):
        board.append([a[i], b[i]])
    return board

def temperature(T):
    return 100 / T

def probability_function(delta, T):
    return math.exp(-delta / T)

def delta_e(current_board, new_board):
    return heuristic(new_board) - heuristic(current_board)

def heuristic(board):
    count = 0
    temp_board = board.copy()
    while temp_board:
        for i in range(1, len(temp_board)):        
            if temp_board[0][1] == temp_board[i][1]:
                count += 1
            if (temp_board[0][0] + temp_board[i][1]) == (temp_board[0][1] + temp_board[i][0]):
                count += 1
            if (temp_board[0][0] + temp_board[0][1]) == (temp_board[i][0] + temp_board[i][1]):
                count += 1
        temp_board.pop(0)
    return count

def random_successor(board):
    new_board = [row[:] for row in board]
    col = random.randrange(8)
    row = random.randrange(8)
    new_board[col][1] = row
    return new_board

def create_population():
    return [create_board() for i in range(16)]

def heuristic_mean(population):
    heuristics = [heuristic(board) for board in population]
    return sum(heuristics) / 16

def natural_selection(population):
    return [board for board in population if heuristic(board) < heuristic_mean(population)]

def mating(board, mate):
    cross = random.randrange(3, 7)
    return board[:cross] + mate[:cross]

def mating_ritual(selected_population):
    post_mating = []
    for board in selected_population:
        mate = selected_population[random.randrange(len(selected_population))]
        offspring = mating(board, mate)
        if heuristic(board) <= heuristic(offspring):
            post_mating.append(board)
        else:
            post_mating.append(offspring)
    return post_mating

def mutation(post_mating):
    for board in post_mating:
        if random.random() < 0.05:
            board[1] = random.random.randrange(8)
    return board

def create_new_population(post_mating):
    needed = 16 - len(post_mating)
    for i in range(needed):
        post_mating.append(create_board())
    return post_mating

def check_for_goal_state(population):
    for board in population:
        if heuristic(board) == 0:
            return board
    return None

main()

