from input_reader import read_data_from_file
from output_writer import write_result
from config import Config
from sympy.parsing import parse_expr
from main_algorithm import annealing_method, wrapped_sympy_function
from test import create_test_cases


def main():
    task_file = "input/task.txt"
    answer_file = "input/ans.txt"
    config_file = "input/config.txt"
    config = Config(config_file)
    data = read_data_from_file(task_file)
    result = annealing_method(wrapped_sympy_function(data[0]), data[1], config=config)
    write_result(result, answer_file)

    test_cases = create_test_cases()
    for i, case in enumerate(test_cases[:-1]):
        print("Iteration # {}".format(i + 1))
        res = annealing_method(wrapped_sympy_function(parse_expr(case.func)), case.x_0, config=config)
        print("Method result: {}; True result: {}".format(res[1], case.expected))


if __name__ == '__main__':
    main()
