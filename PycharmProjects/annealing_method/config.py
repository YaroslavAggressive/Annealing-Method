import traceback
import sys
import ast
from logger import CustomLogger
from decimal import Decimal

REQUIRED_PARAMS = ["mode", "alpha", "T_max", "iter", "step"]

CONFIG_LOGFILE = "logs/config.log"
CONFIG_LOGNAME = "config_logger"
ANNEALING_MODES = {'sub': lambda t, a, k: t - k*a, 'mul': lambda t, a, k: t * a**k,
                   "quad": lambda t, a, k: t / (1 + a * k**2),
                   'log': lambda t, a, k: t / (1 + a * float(Decimal(k + 1).log10()))}


class Config:

    def __init__(self, filename: str):
        self.filename = filename
        self.logger = CustomLogger(log_name=CONFIG_LOGNAME, log_file=CONFIG_LOGFILE)
        self.logger.info_mess("Started creating configuration for method")
        for param in REQUIRED_PARAMS:
            exec("{} = 0".format("self." + param))
        params = self.read_config()
        self.fill_config(params)

    def read_config(self) -> dict:
        self.logger.info_mess("Started reading configurations")

        try:
            file = open(self.filename, "r")
        except IOError:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = str(frame[0]).split()[4]
            self.logger.error_mess(line_number=int(line_err_num))
        with file:
            params = dict()
            lines = file.readlines()
            for line in lines:
                temp_dict = ast.literal_eval(line)
                params.update(temp_dict)

        if len(params) != len(REQUIRED_PARAMS):
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = str(frame[0]).split()[4]
            self.logger.error_mess("Incorrect number of configuration parameters", int(line_err_num))
        self.logger.info_mess("Config parameters read successfully")
        return params

    def fill_config(self, params: dict):
        self.logger.info_mess("Started filling config parameters")
        try:
            for key in params:
                if key not in REQUIRED_PARAMS:
                    frame = traceback.extract_tb(sys.exc_info()[2])
                    line_err_num = str(frame[0]).split()[4]
                    self.logger.error_mess("Unknown parameter name", int(line_err_num))
                str_name = "self." + key
                val = params[key]
                if type(val) == str:
                    exec("{} = '%s'".format(str_name) % val)
                    self.logger.info_mess("Read parameter \" {} \"  with value '{}'".format(key, val))
                else:
                    exec("{} = {}".format(str_name, val))
                    self.logger.info_mess("Read parameter \" {} \"  with value {}".format(key, val))
            self.logger.info_mess("Filling config parameters completed successfully")
        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_err_num = str(frame[0]).split()[4]
            self.logger.error_mess(line_number=int(line_err_num))
