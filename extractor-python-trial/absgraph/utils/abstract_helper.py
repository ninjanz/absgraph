from collections import defaultdict
from itertools import combinations

import json


def map_nodes(current_map):
    """
    A simple function that creates a dictionary with
    the keys as the type of nodes and the values
    as the node id that correponds to that particular type

    :param current_map: utilises the 'nodes' section of the
    input *current_map*

    :return: dictionary
    """
    node_list = defaultdict(list)

    for node in current_map['nodes']:
        node_list[node['type']].append(node['nodeID'])

    return node_list


def find_premises(current_map, nodes):
    """
    Finds premises in the argument map using a simple rule:
    premises are all those that have no incoming arrows from an
    RA node

    :param current_map:
    :param nodes: output of map_nodes()

    :return: list of strings where the strings are the IDs of
     premises
    """
    non_premises = []

    for edge in current_map['edges']:
        if edge['fromID'] in nodes['RA'] and edge['toID'] in nodes['I']:
            non_premises.append(edge['toID'])

    premises = [x for x in nodes['I'] if x not in non_premises]

    return ';'.join(premises)


def find_rules(current_map, nodes):
    """
    Rules are formed by those nodes linked by RA nodes.
    On the left hand side of the rule are all the I nodes that
    are linked TO an RA node. The right hand part of the rule is
    the I node (conclusion) that is linked FROM an RA node.

    :param current_map:
    :param nodes: output of map_nodes()

    :return: a string with all the rules, rules are separated by a semicolon
    eg. [r1] Q1,Q2=>Q3;[r2] Q4=>Q7
    """
    rules = ''

    # iterating through the RA nodes
    for x, node in enumerate(nodes['RA'], start=1):
        from_nodes = []
        to_node = None

        for edge in current_map['edges']:
            # if the edge is pointing to a RA node and from an I node, save it
            if edge['toID'] == node and edge['fromID'] in nodes['I']:
                from_nodes.append(edge['fromID'])

            # likewise if edge is from an RA node and pointing to an I node, save it
            if edge['fromID'] == node and edge['toID'] in nodes['I']:
                to_node = edge['toID']

        if len(from_nodes) != 0 and to_node is not None:
            rules = rules + '[r' + str(x) + '] ' + ','.join(from_nodes) + '=>' + to_node + ';'

    return rules


def find_contrariness(current_map, nodes):
    """
    Function to find the contrariness which can be of two types:
        - contradictory conclusions: double CA link between I nodes, order not important
        - conclusion that is contrary of another conclusion but not the other way round,
            order is important (single CA link)

    :param current_map:
    :param nodes: output of map_nodes()

    :return: a string containing all the contrariness, separated by semicolon
    """
    contrariness = ''
    pairs = []

    for node in nodes['CA']:

        f_node, t_node = None, None
        for x in current_map['edges']:
            if x['toID'] == node and x['fromID'] in nodes['I']:
                f_node = x['fromID']

            if x['fromID'] == node and x['toID'] in nodes['I']:
                t_node = x['toID']

            if f_node is not None and t_node is not None:
                pairs.append((f_node, t_node))
                break

    excess = []
    for a, b in combinations(pairs, 2):
        if set(a) == set(b):
            contrariness += str(a[0]) + '-' + str(a[1]) + ';'
            excess.append(b)

    pairs = [x for x in pairs if x not in set(excess)]

    for f_node, t_node in pairs:
        contrariness += (str(f_node) + '^' + str(t_node) + ';')

    return contrariness


def get_web_input(current_map, nodes):
    """
    Uses the previous functions to and maps their outputs to a dictionary
    which is then parsed to a JSON string, the format required for the servers.

    :param current_map:
    :param nodes: output of map_nodes()

    :return: returns a string version of the dict shown below,
    this is the standard JSON string to send to the server to evaluate maps
    """
    webservice_input = {'transposition': True,
                        'premises': '',
                        'link': 'last',
                        'rules': '',
                        'kbPrefs': '',
                        'semantics': 'preferred',
                        'contrariness': '',
                        'rulePrefs': ''}

    funcs = [find_premises, find_rules, find_contrariness]
    keys = ['premises', 'rules', 'contrariness']

    for f, k in zip(funcs, keys):
        webservice_input[k] = f(current_map, nodes)

    print(webservice_input)
    return json.dumps(webservice_input)


def rename_nodes(input_str, nodes):
    # rename all the nodes to shorter strings
    """
    Renames all the I nodes to shorter strings, the nodes are renamed
    AFTER converting to input string form as then it simplifies the
    renaming process, instead of having to rename ALL the nodes and edges.

    :param nodes: output of map_nodes()
    :param input_str: output of get_web_input()
    :return: the same string with the nodes renamed
    """
    new_names = {}
    for i, node_num in enumerate(nodes['I']):
        new_names[node_num] = 'Q' + str(i)

    print(new_names)
    for k, v in new_names.items():
        input_str = input_str.replace(k, v)

    return input_str



