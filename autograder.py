# Firstname Lastname
# NetID
# COMP 182 Spring 2021 - Homework 8, Problem 2

# You may NOT import anything apart from already imported libraries.
# You can use helper functions from provided.py, but they have
# to be copied over here.

import math
import random
import numpy
from collections import *

#################   PASTE PROVIDED CODE HERE AS NEEDED   #################



#####################  STUDENT CODE BELOW THIS LINE  #####################

def compute_counts(training_data: list, order: int) -> tuple:
	pass

def compute_initial_distribution(training_data: list, order: int) -> dict:
	pass

def compute_emission_probabilities(unique_words: list, unique_tags: list, W: dict, C: dict) -> dict:
	pass

def compute_lambdas(unique_tags: list, num_tokens: int, C1: dict, C2: dict, C3: dict, order: int) -> list:
	pass

def build_hmm(training_data: list, unique_tags: list, unique_words: list, order: int, use_smoothing: bool):
	pass

def trigram_viterbi(hmm, sentence: list) -> list:
	pass
