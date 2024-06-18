# This code is part of Rice COMP182 and is made available for your
# use as a student in COMP182. You are specifically forbidden from
# posting this code online in a public fashion (e.g., on a public
# GitHub repository) or otherwise making it, or any derivative of it,
# available to future COMP182 students.

import traceback
import re
import sys
from collections import defaultdict

print("""DISCLAIMER: This tool is intended to ensure your code is
compatible with the autograder, not that it is correct. It is
possible to 'pass' this tool, yet receive a 0 on the coding portion.
You are still responsible for writing your own tests to ensure the
correctness of your code.
""")

class SkeletonAutograder():
    def __init__(self):
        self._allowed_imports = []
        self._test_cases_functions = []
        self._test_cases_inputs = []
        self._test_cases_expected = []
        self._test_cases_equality = []
        self._test_cases_expected_alternate = []
        self._test_cases_notes = []

    def set_allowed_imports(self, imports: list):
        self._allowed_imports = imports

    def add_test_case(self, function, inputs: list, outputs: list, note = "", equality = lambda x, y, z, w: x == y, alternate_solutions = []):
        self._test_cases_functions.append(function)
        self._test_cases_inputs.append(inputs)
        self._test_cases_expected.append(outputs)
        self._test_cases_equality.append(equality)
        self._test_cases_expected_alternate.append(alternate_solutions)
        self._test_cases_notes.append(note)

    def fail_test(self):
        print("\nFAILED!")
        exit()

    def check_python_version(self):
        """
        Checks the Python version.
        """
        if sys.version_info[0] < 3:
            print("You must run this script using Python 3.")
            exit()
        
        if sys.version_info[1] < 8:
            print("""\nWARNING: Your solution will be graded on Python 3.8, and your version is """ + str(sys.version_info[0])+"."+str(sys.version_info[1])+""". 
            We encourage you to test your code on Python 3.8+ for consistency.\n""")

    def check_imports(self):
        """
        This method verifies that only allowed imports are used in 
        student's submission. Requires 'set_allowed_imports' to be 
        executed before checking.

        If there is an illegal import, then it fails and exits the 
        skeleton autograder.
        """

        # Set regular expression to match Python import statements.
        pattern = re.compile(r"(^from\s(\w+)\simport\s([\w*]+)$)|(^import\s(\w+)$)|^import\s(\w+)\sas\s([\w*]+)$")

        # Define list for illegally used imports.
        illegal_imports = []

        with open("autograder.py") as f:
            lines = f.readlines()
            for line in lines:
                # Match the pattern.
                line = re.sub(r'\s+$', '', re.sub(r'^\s+', '', line))
                match = pattern.match(line)

                # Check for matches.
                if match is not None:
                    groups = match.groups(default='')
                    importstr = " ".join(groups[1:3] if groups[0] else [groups[4]])
                    if importstr not in self._allowed_imports:
                        illegal_imports.append(line)

        if len(illegal_imports) > 0:
            print("A disallowed import was detected. Please remove this import and re-run the autograder.\nThe line(s) in question are:")
            for line in illegal_imports:
                print(line)

            self.fail_test()

    def check_directory(self):
        """
        This method verifies that student submission is in the same directory as the skeleton autograder.

        If the skeleton autograder cannot import 'autograder.py', then it fails and exists the skeleton autograder.
        """
        try:
            import autograder
        except ImportError:
            print("""Failed to import 'autograder.py'.
            Ensure the following:
                1. Your submission is titled 'autograder'.py
                2. Your submitted 'autograder.py' file is in the same directory as this file ('skeleton_autograder.py')
                3. Your submission doesn't import anything other than the imports in the original provided template file
            See the error below for more information:\n"""+traceback.format_exc())

            self.fail_test()

        except Exception:
            print("""Failed to import 'autograder.py'.
            Your code likely failed due to code located outside a function failing.
            Ensure the following:
                1. All of your code is in one of the autograder or helper functions
                2. Any testing code, or code outside of a function, is commented out
            See the error below for more information:\n"""+traceback.format_exc())

            self.fail_test()

    def run_tests(self, run_typechecks = False):
        """
        This method runs all the test cases defined. By default, it checks whether the autograder.py is located in
        the same directory and whether imports are legal.

        Flag run_typechecks can be toggled to
        """

        # Run default tests to ensure form.
        self.check_directory()
        self.check_imports()

        import autograder

        for test_id, func_name in enumerate(self._test_cases_functions):

            # Try to get the function, if the function cannot be located in autograder, then fail the test.
            try:
                func = getattr(autograder, func_name)
            except AttributeError:
                print("Could not locate function '" + func_name + "', ensure your code contains a function with that exact name.")
                print("See the error below for more information:\n")
                print(traceback.format_exc())

                self.fail_test()

            inputs = self._test_cases_inputs[test_id]
            expected = self._test_cases_expected[test_id]
            equality = self._test_cases_equality[test_id]
            alternate = self._test_cases_expected_alternate[test_id]
            notes = self._test_cases_notes[test_id]

            # Run student's function.
            print("Running Test #"+str(test_id)+" on '"+ func_name + "'...")
            try:
                actual = func(*inputs)

                print("Input(s): "+ str(inputs))
                print("Expected Output(s): "+ str(expected))
                print("Actual Output(s)  : "+ str(actual))
                if notes != "":
                    print("** Note: "+ notes)
                print("")

                if run_typechecks and type(expected) is not type(actual):
                    print("Wrong type returned, expecting '" + str(type(expected)) + "', received '" + str(type(actual)) + "'.")

                    self.fail_test()

                if type(expected) == list or type(expected) == tuple:
                    if len(expected) != len(actual):
                        print("Was expecting "+str(len(expected))+" number of output, received "+str(len(actual))+".")

                        self.fail_test()

                if not equality(expected, actual, None, None):
                    if not alternate:
                        print("Wrong value returned, expecting '" + str(expected) + "', received '" + str(actual) + "'.")
                        self.fail_test()
                    else:
                        valid_case = False

                        for acase in range(len(alternate)):
                            if valid_case:
                                break

                            if equality(alternate[acase], actual, None, None):
                                valid_case = True

                        if not valid_case:
                            print("Wrong value returned, expecting '" + str(expected) + "', received '" + str(actual) + "'.")
                            self.fail_test()

                print("Test passed!\n")

            except Exception:
                print("Code failed to run, see the error below for more information:\n")
                print(traceback.format_exc())

                self.fail_test()



skeleton_autograder = SkeletonAutograder()
skeleton_autograder.set_allowed_imports(['math', 'random', 'numpy', 'collections *'])


## COMP 182 Spring 2021 - Homework 8, Problem 2 Test Cases
class HMM:
    """
    Simple class to represent a Hidden Markov Model.
    """

    def __init__(self, order, initial_distribution, emission_matrix, transition_matrix):
        self.order = order
        self.initial_distribution = initial_distribution
        self.emission_matrix = emission_matrix
        self.transition_matrix = transition_matrix

def fill_defaultdict(dd, d):
    for key in d.keys():
        dd[key] = d[key]
    
def fill_nested_defaultdict(dd, d):
    for key0 in d.keys():
        for key1 in d[key0].keys():
            dd[key0][key1] = d[key0][key1]

def fill_double_nested_defaultdict(dd, d):
    for key0 in d.keys():
        for key1 in d[key0].keys():
            for key2 in d[key0][key1].keys():
                dd[key0][key1][key2] = d[key0][key1][key2]

def same_int_or_dictionary(expected, actual, _1, _2):
    """
    Test the equality of the two values. Values can be either ints or dictionaries

    Arguments:
    expected -- The expected input.
    actual -- The student output input
    
    Returns:
    True if the student dictionary is equivalent to the expected dictionary.
    False otherwise.
    """

    expected_is_dict = isinstance(expected, dict)
    actual_is_dict = isinstance(actual, dict)

    if expected_is_dict != actual_is_dict:
        return False
    
    if not expected_is_dict:
        return expected == actual

    return same_dictionary_helper(expected, actual, _1, _2) and same_dictionary_helper(actual, expected, _1, _2)

def same_dictionary_helper(d1, d2, _1, _2):
    for key in d1:
        try:
            if (not same_int_or_dictionary(d1[key], d2[key], _1, _2)):
                return False
        except:
            return False
    return True

def compute_counts_equivalence_checker(expected, actual, _1, _2):
    check_C3 = False
    if len(expected) == 5:
        check_C3 = True
    
    same_num_tokens = expected[0] == actual[0]
    same_W = same_int_or_dictionary(expected[1], actual[1], _1, _2)
    same_C1 = same_int_or_dictionary(expected[1], actual[1], _1, _2)
    same_C2 = same_int_or_dictionary(expected[1], actual[1], _1, _2)
    same_C3 = same_int_or_dictionary(expected[1], actual[1], _1, _2) if check_C3 else True
    
    return same_num_tokens and same_W and same_C1 and same_C2 and same_C3

# Testing Parameters
unique_words = ['hw7', 'is', 'difficult', '.']
unique_tags = ['N', 'V', 'A', '.']
training_data = [('hw7','N'), ('is','V'),('difficult','A'),('.','.')]
num_tokens = 4

_W = {'A': {'difficult': 1}, '.': {'.': 1}, 'V': {'is': 1}, 'N': {'hw7': 1}}
_C1 = {'A': 1, '.': 1, 'V': 1, 'N': 1}
_C2 = {'A': {'.': 1}, 'V': {'A': 1}, 'N': {'V': 1}}
_C3 = {'V': {'A': {'.': 1}}, 'N': {'V': {'A': 1}}}
_initial_distribution2 = {'N': 1}
_initial_distribution3 = {'N': {'V': 1}}
_emission_probabilities = {'A': {'difficult': 1}, '.': {'.': 1}, 'V': {'is': 1}, 'N': {'hw7': 1}}

W = defaultdict(lambda : defaultdict(int))
C1 = defaultdict(int)
C2 = defaultdict(lambda : defaultdict(int))
C3 = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
initial_distribution2 = defaultdict(int)
initial_distribution3 = defaultdict(lambda : defaultdict(int))
emission_probabilities = defaultdict(lambda : defaultdict(int))

fill_nested_defaultdict(W, _W)
fill_defaultdict(C1, _C1)
fill_nested_defaultdict(C2, _C2)
fill_double_nested_defaultdict(C3, _C3)
fill_defaultdict(initial_distribution2, _initial_distribution2)
fill_nested_defaultdict(initial_distribution3, _initial_distribution3)
fill_nested_defaultdict(emission_probabilities, _emission_probabilities)

lambdas = [1, 0, 0]
_trigram_initial_distribution = {'N': {'N': 1}}
_trigram_emission_probabilities = {'N': {'test': 1}}
_trigram_transition_matrix = {'N':{'N':{'N':1}}}

trigram_initial_distribution = defaultdict(lambda : defaultdict(int))
trigram_emission_probabilities = defaultdict(lambda : defaultdict(int))
trigram_transition_matrix = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))

fill_nested_defaultdict(trigram_initial_distribution, _trigram_initial_distribution)
fill_nested_defaultdict(trigram_emission_probabilities, _trigram_emission_probabilities)
fill_double_nested_defaultdict(trigram_transition_matrix, _trigram_transition_matrix)

_trigram_initial_distribution = {'Coin1': {'Coin1': .25, 'Coin2': .25}, 'Coin2': {'Coin1': .25, 'Coin2': .25}}
_trigram_emission_probabilities = {'Coin1': {'Heads': .9, 'Tails': .1}, 'Coin2': {'Heads': .5, 'Tails': .5}}
_trigram_transition_matrix = {'Coin1': {'Coin1': {'Coin1': .5, 'Coin2': .5}, 'Coin2': {'Coin1': .5, 'Coin2': .5}}, 'Coin2': {'Coin1': {'Coin1': .5, 'Coin2': .5}, 'Coin2': {'Coin1': .5, 'Coin2': .5}}}

hmm = HMM(3, _trigram_initial_distribution, _trigram_emission_probabilities, _trigram_transition_matrix)
sentence = ['Heads', 'Heads', 'Tails']
tagged_sentence = [('Heads','Coin1'), ('Heads','Coin1'),('Tails', 'Coin2')]

# compute_counts
skeleton_autograder.add_test_case('compute_counts', [training_data, 2], (num_tokens, W, C1, C2), equality = compute_counts_equivalence_checker)
skeleton_autograder.add_test_case('compute_counts', [training_data, 3], (num_tokens, W, C1, C2, C3), equality = compute_counts_equivalence_checker)

# compute_initial_distribution
skeleton_autograder.add_test_case('compute_initial_distribution', [training_data, 2], initial_distribution2, equality = same_int_or_dictionary)
skeleton_autograder.add_test_case('compute_initial_distribution', [training_data, 3], initial_distribution3, equality = same_int_or_dictionary)

# compute_emission_probabilities
skeleton_autograder.add_test_case('compute_emission_probabilities', [unique_words, unique_tags, W, C1], emission_probabilities, equality = same_int_or_dictionary)

# compute_lambdas
skeleton_autograder.add_test_case('compute_lambdas', [unique_tags, num_tokens, C1, C2, C3, 2], lambdas)
skeleton_autograder.add_test_case('compute_lambdas', [unique_tags, num_tokens, C1, C2, C3, 3], lambdas)

# trigram_viterbi
skeleton_autograder.add_test_case('trigram_viterbi', [hmm, sentence], tagged_sentence)

skeleton_autograder.run_tests(run_typechecks = False)
