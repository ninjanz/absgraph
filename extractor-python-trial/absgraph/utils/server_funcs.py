import requests


def convert_abstract(input_string):

    """
    This function is used to convert the graphs in to abstract form

    :param input_string: a json string that has the attributes:
            - transposition
            - premises
            - link
            - rules
            - kbPrefs
            - semantics
            - contrariness
            - rulePrefs

    :return: a json string that contains these attributes:
            - defeats
            - arguments
    """
    link = 'http://localhost:8080/web_service_war_exploded/helloworld/abstract/'
    r = requests.post(url=link, data=input_string)

    if r.status_code == requests.codes.ok:
        return r.text
    elif r.status_code == 415:
        print('Error ' + str(r.status_code) + ': Wrong input format')
    elif r.status_code == 400:
        print('Error ' + str(r.status_code) + ': Server offline!')

    return None


def evaluate(input_string):

    """
    This function is used to convert the graphs in to abstract form with more details

    :param input_string: a json string that has the attributes:
            - transposition
            - premises
            - link
            - rules
            - kbPrefs
            - semantics
            - contrariness
            - rulePrefs

    :return: a json string that contains these attributes:
            - well formed
            - defeats
            - extensions
            - arguments (links)

    """
    link = 'http://localhost:8080/web_service_war_exploded/helloworld/evaluate/'
    r = requests.post(url=link, data=input_string)

    if r.status_code == requests.codes.ok:
        return r.text
    elif r.status_code == 415:
        print('Error ' + str(r.status_code) + ': Wrong input format')
    elif r.status_code == 400:
        print('Error ' + str(r.status_code) + ': Server offline!')

    return None


def eval_toast(input_string):
    link = 'http://toast.arg-tech.org/api/evaluate'
    r = requests.post(url=link, data=input_string)

    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print('Error')

    return None
