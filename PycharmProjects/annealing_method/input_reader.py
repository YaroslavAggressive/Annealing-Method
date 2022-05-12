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

        if len(data) != 2:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = (frame[0]).split()[4]
            message = "Redundancy of the initial data on the problem, check the input" if len(data) > 3 \
                else "Not enough data for the problem statement, check the input"
            logger.error_mess(message, line_err_num)

        try:
            func = sympy_parser.parse_expr(data[0], evaluate=False)
            logger.info_mess("Successfully parsed target function from input")
            logger.info_mess("Target function problem: F = {}".format(func))
        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = (frame[0]).split()[4]
            logger.error_mess(line_number=line_err_num)

        try:
            # parsing x_0 as list from str
            x_0 = ast.literal_eval(str(data[1]))
            logger.info_mess("Successfully parsed initial state from input")
            logger.info_mess("Initial state value: x_0 = {}".format(x_0))
        except ValueError:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = (frame[0]).split()[4]
            logger.error_mess(line_number=line_err_num)

        logger.info_mess("Reading input data completed successfully")
        logger.info_mess("Number of input strings read: {}".format(len(data)))
        return [func, x_0]


