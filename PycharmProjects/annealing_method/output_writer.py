from logger import CustomLogger
import sys
import traceback


WRITER_LOGFILE = "logs/writer.log"
WRITER_LOGNAME = "writer_logger"


def write_result(result_data: list, filename: str):
    logger = CustomLogger(log_name=WRITER_LOGNAME, log_file=WRITER_LOGFILE)
    logger.info_mess("Started writing result")
    # обработать ошибку неверного имени файла или некорректной передачи данных
    try:
        file = open(filename, "w")
    except IOError:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_err_num = str(frame[0]).split()[4]
        logger.error_mess(line_number=int(line_err_num))

    with file:  # обработать ошибку открытия файла
        file.write("Solution found after {} iterations\n".format(result_data[2]))
        file.write("Optimum point is: x* = {}\n".format(result_data[0]))
        file.write("Target function value at optimum point: F(x*) = {}\n".format(result_data[1]))
        logger.info_mess("Completed writing result")
