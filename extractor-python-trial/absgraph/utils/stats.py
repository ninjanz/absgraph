import absgraph.utils.server_funcs as abs_s
from itertools import combinations

import json
import time


def stats_counter(abstract, eval_form, input_str):

    def count_nodes():
        return len(abstract['arguments'])

    def count_edges():
        return len(abstract['defeats'])

    def count_rules():
        return len(input_str['rules'].split(';'))-1

    def count_extensions():
        return len(eval_form['extensions'])

    def count_contrariness():
        contradictory, contrary = 0, 0

        for x in input_str['contrariness'].split(';'):
            if '-' in x:
                contradictory += 1
            elif '^' in x:
                contrary += 1
            else:
                continue

        return [contradictory, contrary]

    def count_cycles():
        count = 0
        involved = []

        for attack in abstract['defeats']:
            involved.append(attack.split('>'))
        print(involved)

        for a, b in combinations(involved, 2):
            if set(a) == set(b):
                count += 1

        return count

    def calculate_density():
        e = count_edges()
        v = count_nodes()

        try:
            return e / (v * (v - 1))
        except ZeroDivisionError:
            return 0

    def calculate_eval_time():
        time_ws = []
        time_toast = []

        for i in range(3):
            st = time.time()
            abs_s.eval_toast(json.dumps(input_str))
            time_toast.append(time.time() - st)

        for i in range(3):
            st = time.time()
            abs_s.evaluate(json.dumps(input_str))
            time_ws.append(time.time() - st)

        avg_time_1 = sum(time_ws) / 3
        avg_time_2 = sum(time_toast) / 3

        return [avg_time_1, avg_time_2]

    return {
        'n_nodes': count_nodes(),
        'n_edges': count_edges(),
        'n_cycles': count_cycles(),
        'n_ext': count_extensions(),
        'n_rules': count_rules(),
        'n_contrary': count_contrariness(),
        'density': calculate_density(),
        'avg_eval_time': calculate_eval_time()
    }
