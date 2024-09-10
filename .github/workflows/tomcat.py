import os, os.path
import requests
import logging
import time, socket
import sys

log_tomcat_module = logging.getLogger("tomcat.py")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


def check_tomcat_status():
    return os.system('systemctl is-active --quiet tomcat.service')


def wait_for_port(host, port):
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port)):
                break
        except OSError as e:
            if time.perf_counter() - start_time >= 300:
                log_tomcat_module.error(
                    'Waited too long for the port {} on host {} to start accepting connections. Error: {} '.format(port,
                                                                                                                   host,
                                                                                                                   e.strerror))
                sys.exit(1)


def print_url_status(host, port):
    url = "http://"+ host + ":" + port
    log_tomcat_module.info("Status Code returned for URL: " + url + " is " + str(requests.get(url).status_code))


def start_tomcat_service(host, port):
    log_tomcat_module.info('Checked into start_tomcat_service')
    if not (check_tomcat_status() == 0):
        try:
            log_tomcat_module.info("Starting: Tomcat Service")
            os.system('sudo systemctl start --quiet tomcat.service')
            if check_tomcat_status() == 0:
                log_tomcat_module.info("Tomcat Started successfully")
                wait_for_port(host, port)
                print_url_status(host, port)
        except OSError as e:
            log_tomcat_module.error("Error:" + e.strerror)
            sys.exit(1)
    else:
        log_tomcat_module.info("Tomcat already in RUNNING state")


def stop_tomcat_service():
    log_tomcat_module.info('Checked into stop_tomcat_service')
    if check_tomcat_status() == 0:
        try:
            log_tomcat_module.info("Stopping: Tomcat Service")
            os.system("sudo systemctl stop --quiet tomcat.service")
            if not (check_tomcat_status() == 0):
                log_tomcat_module.info("Tomcat Stopped successfully")
        except OSError as e:
            log_tomcat_module.error("Error:" + e.strerror)
            sys.exit(1)
    else:
        log_tomcat_module.info("Tomcat already in STOPPED state")


if __name__ == '__main__':
    if sys.argv.__len__() >= 2:
        if sys.argv.__len__() == 4 and sys.argv[1] == 'start':
            host = sys.argv[2]
            port = sys.argv[3]
            log_tomcat_module.info("Calling function start_tomcat_service")
            start_tomcat_service(host, port)
        elif sys.argv[1] == 'stop':
            log_tomcat_module.info("Calling function stop_tomcat_service")
            stop_tomcat_service()
        else:
            log_tomcat_module.error("Incorrect input. Acceptable arguments: start <URL> <port> or stop ")
            sys.exit(1)
    else:
        log_tomcat_module.error("Incorrect input. Acceptable arguments: start <URL> <port> or stop ")
        sys.exit(1)
