def make(gen_dir):
    """
    Performs all the calculations, plotting, etc. necessary to generate the reports.

    :param gen_dir: The directory to store generate files like images
    :return: The context for template rendering, containing whatever information the reports need
    :rtype: dict
    """
    context = {
        'name': 'Ben'
    }

    return context
