from typing import Callable, Any
from scipy.stats import binom, truncnorm
from math import exp
import numpy as np
from numpy.random import choice
from copy import deepcopy
import traceback
import sys
from random import random
from scipy.constants import k  # Boltzmann constant

from logger import CustomLogger
from config import Config, ANNEALING_MODES

ANNEALING_LOGFILE = "logs/annealing.log"
ANNEALING_LOGNAME = "annealing_logger"
ITERATIONS_PER_LOG_MESSAGE = 100


def wrapped_sympy_function(sympy_func: Any):
    return lambda x_dict: sympy_func.subs([(x_i, x_dict[str(x_i)]) for x_i in sympy_func.free_symbols])


def get_truncated_normal(mean=0, sd=1, low=0, upp=10, logger: CustomLogger = None):
    try:
        return truncnorm(
            (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
    except:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_err_num = str(frame[0]).split()[4]
        logger.error_mess("Error using truncated normal distrib", line_number=int(line_err_num))


def random_state_change(point: dict, step: float, dim: int, logger: CustomLogger) -> np.array:
    try:
        new_point = deepcopy(point)
        keys = list(point.keys())
        if dim > 1:
            changing_dimensions = choice(list(range(len(point))), dim // 2)
            for i in changing_dimensions:
                key = keys[i]
                new_point[key] = point[key] + step
        else:
            key = keys[0]
            new_point[key] = point[key] + step
        return new_point
    except:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_err_num = str(frame[0]).split()[4]
        logger.error_mess(line_number=int(line_err_num))


def annealing_method(func: Callable, x_0: dict, config: Config) -> (np.array, float):
    logger = CustomLogger(log_name=ANNEALING_LOGNAME, log_file=ANNEALING_LOGFILE)
    logger.info_mess("Starting optimization process")
    t = config.T_max
    iter_quan = config.iter
    n = len(x_0)  # number of optimization measurements
    logger.info_mess("Number of minimization dimensions: {}".format(n))
    best = x_0
    logger.info_mess("Initial argument statement: x_0 = {}".format(best))
    best_fit = func(best)
    logger.info_mess("Initial target function value: F(x_0) = {}".format(best_fit))
    i = 0
    try:
        for i in range(iter_quan):
            step_distribution = get_truncated_normal(mean=0, sd=1, low=-1, upp=1, logger=logger)
            step = config.step * step_distribution.rvs(size=1)[0]
            x_trial = random_state_change(best, step, n, logger)
            delta = func(x_trial) - best_fit
            if delta <= 0:
                best = x_trial
                best_fit = func(best)
            elif exp(-delta / t) > random():
                best = x_trial
                best_fit = func(best)
            if i + 1 % ITERATIONS_PER_LOG_MESSAGE == 0:
                logger.info_mess("Iteration # {}".format(i + 1))
                logger.info_mess("Best state value: x_best = {}".format(best))
                logger.info_mess("Best target function value: F_best = {}".format(best_fit))
                logger.info_mess("Current temperature: T = {}".format(t))
            t = ANNEALING_MODES[config.mode](config.T_max, config.alpha, i + 1)
        logger.info_mess("Method successfully completed optimization")
        logger.info_mess("Number of iterations: {}".format(i))
        logger.info_mess("Optimum: x* =  {}".format(best))
        logger.info_mess("Optimal target value: F(x)={}".format(best_fit))
        return best, best_fit, i
    except:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_err_num = str(frame[0]).split()[4]
        logger.error_mess(line_number=int(line_err_num))

