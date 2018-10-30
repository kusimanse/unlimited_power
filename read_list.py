from power import Power

def get_power_dict():
	power_list = [l.strip() for l in open('power_list.txt')]

	color = ['c']

	power_dict = {}

	for l in power_list:
		if len(l) <= 2:
			color = list(l)
			continue
		name = l
		if 'Sigil' in name:
			power_dict[name] = Power(name=name, color=color)
		else:
			power_dict[name] = Power(name=name, color=color, t='nonbasic power')
	return power_dict


def read_exported_list(file_name):
	f = [l for l in open(file_name)]
	cards = [' '.join(l.strip().split()[1:][:-2]) for l in f]
	counts = [int(l.split()[0]) for l in f if len(l.split()) > 1]
	power_dict = get_power_dict()
	power_base = []
	for idx, card in enumerate(cards):
		if 'MARKET' in card:
			break
		if card in power_dict:
			for useless in range(counts[idx]):
				power_base.append(power_dict[card])
	non_power = []
	
	return power_base