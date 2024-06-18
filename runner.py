"""
This module includes the wrapper for all test runners, which defines their
interface.
"""
from datetime import datetime 
import logging
import os 

from leotest.errors import RunnerError

_logger = logging.getLogger(__name__)

class LeotestRunner:
    """
    LeotestRunner is the superclass of all test runner plugins, and largely
    defines their interface to the rest of Leotest.

    ####Arguments
    * `title`: The name of this runner
    * `description`: A string describing this runner
    * `config`: A configuration dictionary passed to this instance
    * `data_cb`: The callback function that receives the test results
    """
    def __init__(self, name, title, description="", config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        self.name = name
        self.title = title
        self.description = description
        self._config = config
        self._data_cb = data_cb
        self._location = location
        self._network_type = network_type
        self._connection_type = connection_type
        self._device_id = device_id
        self._route_enabled = False

    def write_raw_stdout(self, output, artifact_path, filename="raw_stdout.log"):
        # write stdout
        raw_stdout = os.path.join(artifact_path, filename)
        print('Writing raw_stdout to {}'.format(raw_stdout))
        _logger.info('Writing raw_stdout to {}'.format(raw_stdout))
        with open(raw_stdout, 'w', encoding='utf-8') as f:
            f.write(output.stdout)

    def _start_test(self, artifact_name):
        raise RunnerError(self.title, "No _start_test() function implemented.")

    def start_test(self):
        """Starts this test, wraps the actual start function."""
      
        # timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        # artifact_name = "{}-{}".format(self.name, timestamp)
        artifact_path_list = [
            self._config["artifacts"]["path_local"],
            self.name
        ]

        self.artifact_path = os.path.join(*artifact_path_list)

        if not os.path.exists(self.artifact_path):
            os.makedirs(self.artifact_path)

        data = self._start_test(self.name)
        return data

    def _stop_test(self):
        _logger.debug("No special handling needed for stopping runner %s",
                      self.title)

    def stop_test(self):
        """Stops this test, wraps the actual stop function (optional)."""
        return self._stop_test()

    def _teardown(self):
        _logger.debug("No special teardown needed for runner %s", self.title)

    def teardown(self):
        """Any final deconstruction for this runner (optional)."""
        return self._teardown()