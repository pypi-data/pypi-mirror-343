import subprocess
import multiprocessing
from swc_utils.exceptions.package_exceptions import MissingDependencyError

try:
    from flask import Flask
except ImportError:
    raise MissingDependencyError("flask")


class WsgiRunner:
    def __init__(self, host: str, port: int or str, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug

    def run_internal(self, application: Flask, *args, **kwargs):
        application.run(host=self.host, port=self.port, debug=self.debug, *args, **kwargs)

    def run_gunicorn(self, application_pointer: str = "__init__:app", backend: str = "gevent", extra_options: dict = None):
        try:
            import gunicorn, gevent
        except ImportError:
            raise MissingDependencyError(["gunicorn", "gevent"], alt_source="web_production")

        if extra_options is None:
            extra_options = {
                "limit-request-line": 0,
                "limit-request-field_size": 0,
                "timeout": 120
            }

        command = [
            "gunicorn",
            "-b", f"{self.host}:{self.port}",
            "-k", backend
        ]

        for key, value in extra_options.items():
            command.extend([f"--{key}", str(value)])

        command.append(application_pointer)

        subprocess.run(command)

    def run_threaded_gunicorn(
            self, threads: int,
            application_pointer: str = "__init__:app", backend: str = "gevent", extra_options: dict = None
    ):
        def thread_func():
            wsgi = self.__class__(self.host, self.port + i, self.debug)
            wsgi.run_gunicorn(application_pointer, backend, extra_options)

        for i in range(threads):
            thread = multiprocessing.Process(target=thread_func)
            thread.start()

    def run_multiprocess_gunicorn(
            self, processes: int,
            application_pointer: str = "__init__:app", backend: str = "gevent", extra_options: dict = None
    ):
        processes = min(processes, multiprocessing.cpu_count())

        def process_func(wsgi_args, gunicorn_args):
            wsgi = self.__class__(*wsgi_args)
            wsgi.run_gunicorn(*gunicorn_args)

        for i in range(processes):
            process = multiprocessing.Process(target=process_func, args=(
                (self.host, self.port + i, self.debug),
                (application_pointer, backend, extra_options)
            ))
            process.start()
