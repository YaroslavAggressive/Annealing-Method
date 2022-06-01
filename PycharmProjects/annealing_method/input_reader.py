from sympy.parsing import sympy_parser
from logger import CustomLogger
import traceback
import sys
import ast

READER_LOGFILE = "logs/reader.log"
READER_LOGNAME = "reader_logger"


def read_data_from_file(filename: str) -> list:
    logger = CustomLogger(log_file=READER_LOGFILE, log_name=READER_LOGNAME)
    logger.info_mess("Started reading input task data")

    try:
        source_file = open(filename, "r")
    except IOError:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_err_num = str(frame[0]).split()[4]
        logger.error_mess(line_number=int(line_err_num))

    with source_file:
        data = []
        for line in source_file:
            if not line.isspace():
                data.append(line)

        try:  # reading function from first file string
            func = sympy_parser.parse_expr(data[0], evaluate=False)
            logger.info_mess("Successfully parsed target function from input")
            logger.info_mess("Target function problem: F = {}".format(func))
        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = str(frame[0]).split()[4]
            logger.error_mess(line_number=int(line_err_num))

        try:
            # parsing x_0 as dict from str
            x_0 = ast.literal_eval(str(data[1]))
            logger.info_mess("Successfully parsed initial state from input")
            logger.info_mess("Initial state value: x_0 = {}".format(x_0))
        except ValueError:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = str(frame[0]).split()[4]
            logger.error_mess(line_number=int(line_err_num))

        try:
            # constraints for each variable in solving task
            var_interval_dict = dict()
            for line in data[2:]:  # смотрим неотпарсенные оставшиееся строки
                lexemes = [lex.strip() for lex in line.split(sep=':')]

                if len(lexemes) != 2:  # checking too much data for constraint error
                    frame = traceback.extract_tb(sys.exc_info()[2])
                    line_err_num = str(frame[0]).split()[4]
                    message = "Too much lexemes in constraint, please, check input"
                    logger.error_mess(message, int(line_err_num))

                tmp_var = lexemes[0]
                tmp_interval = ast.literal_eval(lexemes[1])

                var_list = [str(symb) for symb in func.free_symbols]
                if tmp_var not in var_list:  # checking incorrect variable in constraints error
                    frame = traceback.extract_tb(sys.exc_info()[2])
                    line_err_num = str(frame[0]).split()[4]
                    message = "Can't find variable from constraints in tack function, please, check input"
                    logger.error_mess(message, int(line_err_num))

                if len(tmp_interval) != 2 or tmp_interval[0] > tmp_interval[1]: # checking incorrect interval error
                    frame = traceback.extract_tb(sys.exc_info()[2])
                    line_err_num = str(frame[0]).split()[4]
                    message = "Incorrect variable constraint, please, check input"
                    logger.error_mess(message, int(line_err_num))

            logger.info_mess("Successfully parsed initial state from input")
            logger.info_mess("Initial state value: x_0 = {}".format(x_0))
        except ValueError:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = (frame[0]).split()[4]
            logger.error_mess(line_number=line_err_num)

        logger.info_mess("Reading input data completed successfully")
        logger.info_mess("Number of input strings read: {}".format(len(data)))
        return [func, x_0]


