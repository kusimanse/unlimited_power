import numpy as np

def calculate_statistics(runs, num_runs, target={}):
	#target: the target power base.  For example, hh is {'s':2, 'f':2, 'p': 1} (maybe p is 2?)
	expected = {'P':0, 'F': 0, 'J': 0, 'S': 0, 'T': 0, 'total': 0}
	probabilities = {'P':0, 'F': 0, 'J': 0, 'S': 0, 'T': 0, 'total': 0}
	double_power_probs =  {'P':0, 'F': 0, 'J': 0, 'S': 0, 'T': 0, 'total': 0}
	target_probs = []
	for key in expected:
		expected[key] =  [sum([x[key] for x in y])/num_runs for y in runs]
		probabilities[key] = [sum([x[key] >= 1 for x in y])/num_runs for y in runs]
		double_power_probs[key] =  [sum([x[key] >= 2 for x in y])/num_runs for y in runs]

	if target:
		turn_count = 0
		for turn in runs:
			hit_count = 0
			for sample in turn:
				hit = True
				for key in target:
					if sample[key] < target[key]:
						hit = False
				if hit:
					hit_count += 1
			target_probs.append(hit_count/num_runs)
			turn_count += 1

	return expected, probabilities, double_power_probs, target_probs
