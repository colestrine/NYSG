"""
log_test tests functions in log
"""
import random
import datetime
from log import log, init_log, MAX_SIZE
from pin_constants import load_data


def log_test(log_path, n_iter):
    """
    log_test() tests the log function
    """
    init_log(log_path)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, MAX_SIZE)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, MAX_SIZE)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, MAX_SIZE)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, MAX_SIZE)

    loaded_data = load_data(log_path)
    assert len(loaded_data) == 4 * n_iter


def log_test2(log_path, n_iter):
    """
    log_test() tests the log function
    """
    init_log(log_path)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, 100)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, 100)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, 100)

    test_dict = {}
    for _ in range(n_iter):
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%-S:%f")
        random_data = random.randint(0, 10)
        test_dict[current_time] = random_data
    log(log_path, test_dict, 100)


# -------- MAIN TEST ---------
if __name__ == "__main__":
    DO_TEST = True
    LOG_PATH = "test/log_test.json"
    LOG_PATH2 = "test/log_test2.json"
    N_ITER = 100
    if DO_TEST:
        log_test(LOG_PATH, N_ITER)
        log_test2(LOG_PATH2, N_ITER)
