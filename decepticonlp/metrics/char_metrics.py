import numpy as np


def levenshtein(text1, text2, normalize="none"):
    """
    Calculate Levenshtein Distance using dynamic programming optimized with (np)
    DP - O(m*n) complexity - Recursive approach - O(3^m)

    Example:
    from perturb import levenshtein
    print(levenshtein("Hey","HEY"))
    2.0

    #Normalize Levenshtein Distance - Total strategy
    print(levenshtein("Hey", "HEY", normalize="sum"))
    0.33333

    #Normalize LCS - Max Strategy
    print(levenshtein("HeyS", "HEY", normalize="lcs"))
    0.75


    :params
    :text1, text2 - Both the inputs
    :normalize - Pass "none" for getting the raw distance
               - Pass "sum" for getting Normalized Levenshtein Distance
               - Pass "lcs" for getting #Normalize LCS
    
    returns levenshtein distance

    IMPORTANT NOTE :
    The normalized distance is not a metric, as it violates the triangle inequality.
    https://stackoverflow.com/questions/45783385/normalizing-the-edit-distance
    """

    size_x, size_y = len(text1) + 1, len(text2) + 1
    matrix = np.zeros((size_x, size_y))
    x, y = np.arange(size_x), np.arange(size_y)
    matrix[x, 0] = x
    matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if text1[x - 1] == text2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1, matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1
                )
    distance = matrix[size_x - 1, size_y - 1]
    if normalize == "sum":
        return distance / (size_x + size_y - 2)
    elif normalize == "lcs":
        return distance / (max(size_x, size_y) - 1)
    else:
        return matrix[size_x - 1, size_y - 1]
