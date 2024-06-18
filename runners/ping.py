import logging
import shutil
import json
import os

import pingparsing
from textwrap import dedent

from leotest.errors import RunnerError
from leotest.runner import LeotestRunner
from leotest.utils import execute

logger = logging.getLogger(__name__)

class PingClient(LeotestRunner):
    """Run ping tests."""

    def __init__(self, testname, config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        super().__init__(
            name = testname, 
            title="Ping",
            description="Run simple ping test",
            config=config,
            data_cb=data_cb,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            device_id=device_id)

    @staticmethod
    def _parse_summary(output):
        """Parses the ping summary.

        Args:
            output: stdout of the process

        Returns:
            A dict containing a summary of the test.

        Raises:
            JSONDecodeError: if the output cannot be parsed as JSON.
        """
        leotest_output = {}

        if output.returncode == 0:
            parser = pingparsing.PingParsing()
            stats = parser.parse(dedent(output.stdout))
            leotest_output = stats.as_dict()
            leotest_output["icmp_replies"] = stats.icmp_replies

            return leotest_output
        else:
            
            # Set TestError and every other field to None.
            leotest_output = {
                "destination": None,
                "packet_transmit": None,
                "packet_receive": None,
                "packet_loss_count": None,
                "packet_loss_rate": None,
                "rtt_min": None,
                "rtt_avg": None,
                "rtt_max": None,
                "rtt_mdev": None,
                "packet_duplicate_count": None,
                "packet_duplicate_rate": None,
                "icmp_replies": []
            }
            
        return leotest_output
        
    def _start_test(self, artifact_name):
        logger.info("Starting ping test...")
        if shutil.which("ping") is not None:

            ip = self._config["tests"][self.name]["ip"]
            num_pings = self._config["tests"][self.name]["num_pings"]
            timeout = self._config["tests"][self.name]["test_length"]

            if num_pings:
                starttime, endtime, output = execute("ping", ip, 
                                                    "-c", str(num_pings))
            else:
                starttime, endtime, output = execute("ping", ip, 
                                                    "-w", str(timeout))
            # write stdout
            self.write_raw_stdout(output, self.artifact_path)
            
            leotest_output = {
                'TestName': self.name,
                'TestStartTime': starttime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'TestEndTime': endtime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'LeotestLocation': self._location,
                'LeotestConnectionType': self._connection_type,
                'LeotestNetworkType': self._network_type,
                'LeotestDeviceID': self._device_id,
            }

            leotest_output.update(self._parse_summary(output))

            # write stdout
            metadata = os.path.join(self.artifact_path, "metadata.log")
            logger.info('Writing metadata to {}'.format(metadata))

            with open(metadata, 'w', encoding='utf-8') as f:
                json.dump(leotest_output, f, ensure_ascii=False, indent=4)
            
            return json.dumps(leotest_output)

        else:
            raise RunnerError(
                "ping",
                "Executable does not exist, please install ping.")