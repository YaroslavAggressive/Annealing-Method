from input_reader import read_data_from_file
from output_writer import write_result
from config import Config
from logger import CustomLogger
from main_algorithm import annealing_method, wrapped_sympy_function


def main():
    task_file = "task.txt"
    answer_file = "ans.txt"
    config_file = "config.txt"
    config = Config(config_file)
    data = read_data_from_file(task_file)
    result = annealing_method(wrapped_sympy_function(data[0]), data[1], config=config)
    write_result(result, answer_file)


if __name__ == '__main__':
    main()
