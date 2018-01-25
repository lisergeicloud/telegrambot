import wolframalpha
from mytokens import wolfram_token

client = wolframalpha.Client(wolfram_token)

SOLUTIONS = ['Solution', 'RealSolution', 'ComplexSolution', 'IndefiniteIntegral', 'DefiniteIntegral', 'Result']


def ask(query):
    solutions_dict = {}
    solution = None
    res = client.query(query)
    for pod in res.pods:
        print(pod)
        if pod['@id'] in SOLUTIONS:
            subpod = pod['subpod']
            if isinstance(subpod, list):
                solution_list = [s['plaintext'] for s in subpod]
                solution = '; '.join(solution_list)
            else:
                solution = subpod['plaintext']
            solutions_dict[pod['@id']] = solution
    for s in SOLUTIONS:
        solution = solutions_dict.get(s, None)
        if solution is not None:
            break
    return solution


if __name__ == '__main__':
    solution = ask('derivative sin(x) dx')
    print(solution)
