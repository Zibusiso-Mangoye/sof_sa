import logging

def logger(log_file):
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    #Setup File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    #Setup Stream Handler (i.e. console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.INFO)

    #Get our logger
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    #Add both Handlers
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    return log
