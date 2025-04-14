
def iscube(a):
    '''
    Write a function that takes an integer a and returns True 
    if this ingeger is a cube of some integer number.
    Note: you may assume the input is always valid.
    Examples:
    iscube(1) ==> True
    iscube(2) ==> False
    iscube(-1) ==> True
    iscube(64) ==> True
    iscube(0) ==> True
    iscube(180) ==> False
    '''


    a = abs(a)
    return int(round(a ** (1. / 3))) ** 3 == a





import numpy as np

def is_floats(x) -> bool:
    # check if it is float; List[float]; Tuple[float]
    if isinstance(x, float):
        return True
    if isinstance(x, (list, tuple)):
        return all(isinstance(i, float) for i in x)
    if isinstance(x, np.ndarray):
        return x.dtype == np.float64 or x.dtype == np.float32
    return False


def assertion(out, exp, atol):
    exact_match = out == exp

    if atol == 0 and is_floats(exp):
        atol = 1e-6
    if not exact_match and atol != 0:
        assert np.allclose(out, exp, rtol=1e-07, atol=atol)
    else:
        assert exact_match


def check(candidate):
    inputs = [[1], [2], [-1], [64], [180], [1000], [0], [1729], [1728], [-8], [27], [125], [729], [512], [-27], [-64], [1000000], [-1000000], [120], [57], [-63], [510], [728], [999999], [-999999], [55], [123], [56], [26], [-1000001], [730], [-7], [119], [-28], [126], [-6], [-62], [58], [-5], [727], [-26], [-39], [-1000002], [-46], [999998], [726], [731], [54], [725], [-29], [59], [-47], [31], [25], [509], [124], [-40], [511], [99], [45], [-45], [-999997], [121], [-48], [4], [732], [-726], [1111], [1331], [-13824], [1000000000], [-1000000000], [987654321], [-987654321], [-13825], [-987654320], [-987654319], [-13823], [-727], [-729], [-1000000001], [1332], [3], [-25], [987654322], [-725], [5], [1112], [6], [-1000000002], [7], [-68], [999999999], [-728], [-24], [-724], [-13822], [-987654322], [1110], [8], [-69], [-70], [-723], [-730], [999999998], [-23], [10], [-13821], [1113], [122], [-987654318], [1330], [-1000000003], [-1000000004], [-71], [9], [81], [-22], [999999997], [-21], [-987654317], [-75], [999999996], [-73], [-13826], [-2], [-13820], [82], [987654320], [1109], [28], [-41], [46], [-1000], [99999999999999999999999999], [-99999999999999999999999999], [-1729], [-2147483648], [2147483647], [9223372036854775807], [-9223372036854775808], [1000000001], [127], [1108], [1333], [130], [128], [129], [1107], [1334], [32], [1336], [1000000002], [-18], [1000000003], [30], [-19], [117], [69], [118], [1000000004], [-999999998], [-94], [29]]
    results = [True, False, True, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    for i, (inp, exp) in enumerate(zip(inputs, results)):
        assertion(candidate(*inp), exp, 0)

check(iscube)

