# -*- coding: utf-8 -*-


def extract_currency_from_text(words: str) -> str:
    """

    some variables:
    chart.trades.BTC-PERPETUAL.1
    incremental_ticker.BTC-4OCT24
    """

    if "." in words:
        filter1 = (words.partition(".")[2]).lower()

        if "." in filter1:
            filter1 = (filter1.partition(".")[2]).lower()

            if "chart.trades" in words:
                filter1 = (words.partition(".")[2]).lower()

            if "." in filter1:
                filter1 = (filter1.partition(".")[2]).lower()

                if "." in filter1:
                    filter1 = (filter1.partition(".")[0]).lower()

    else:
        filter1 = (words.partition(".")[0]).lower()

    return (filter1.partition("-")[0]).lower()


def message_template() -> str:
    """ """

    result = {}
    result.update({"params": {}})
    result.update({"method": "subscription"})
    result["params"].update({"data": None})
    result["params"].update({"channel": None})
    result["params"].update({"stream": None})

    return result


def extract_integers_from_text(words: list) -> int:
    """
    Extracting integers from label text. More general than get integer in parsing label function
    """

    words_to_str = str(
        words
    )  # ensuring if integer used as argument, will be returned as itself

    return int("".join([o for o in words_to_str if o.isdigit()]))


def remove_double_brackets_in_list(data: list) -> list:
    """_summary_

    Args:
        data (list): instance: [
                                ['BTC-30AUG24', 'BTC-6SEP24', 'BTC-27SEP24', 'BTC-27DEC24',
                                'BTC-28MAR25', 'BTC-27JUN25', 'BTC-PERPETUAL'
                                ],
                                ['ETH-30AUG24', 'ETH-6SEP24', 'ETH-27SEP24', 'ETH-27DEC24',
                                'ETH-28MAR25', 'ETH-27JUN25', 'ETH-PERPETUAL'
                                ]
                                ]

    Returns:
        list: _description_

    Reference:
        https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    """
    return [o for os in data for o in os]


def remove_apostrophes_from_json(json_load: list) -> int:
    """ """
    import ast

    return [ast.literal_eval(str(i)) for i in json_load]


def remove_redundant_elements(data: list) -> list:
    """
    Remove redundant items in a list

    Args:
        data (list)

    Returns:
        list:

    Example:
        data_original = ['A', 'A', 'B', 'B', 'B', 'C']
        data_cleaned = ['A','B','C']

    Reference:
        1. https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
        2. https://python.plainenglish.io/how-to-remove-duplicate-elements-from-lists-without-using-sets-in-python-5796e93e6d43
    """

    # Create an empty list
    result = []

    # Check if the data is a list and not empty
    if isinstance(data, list) and data != []:
        try:
            # Ref 1
            result = list({frozenset(item.items()): item for item in data}.values())

        except:
            # Ref 2
            result = list(dict.fromkeys(data))

    return result
