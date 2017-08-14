def convert(abstract_form):

    """
    This function is used to convert the abstract format
    of the argument in to both aspartix and trivial graph formats

    :param abstract_form:
    :return: dictionary containing strings of the two formats
    """

    def tgf_format():
        graph_tgf = ''

        for argument in abstract_form['arguments']:
            graph_tgf += argument + '\n'

        graph_tgf += '#\n'

        for attack in abstract_form['defeats']:
            graph_tgf += attack.split('>')[0] + ' ' + attack.split('>')[1] + '\n'

        return graph_tgf

    def aspartix_format():
        graph_apx = ''

        for argument in abstract_form['arguments']:
            # arg(A1).
            # arg(A2).
            graph_apx += 'arg(' + argument + ').' + '\n'

        for attack in abstract_form['defeats']:
            # att(A1,A2).
            att = attack.split('>')
            graph_apx += 'att(' + att[0] + ',' + att[1] + ').' + '\n'

    return {
        'tgf': tgf_format(),
        'apx': aspartix_format()
    }
