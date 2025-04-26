# cnsstat

Cheap-n-nasty text system status via psutil:

	$ cnsstat
	Load: 4 %, 0.1, 0.1, 0.0
	Temp: 41.0 °C
	Mem: 46 %, 1.3/4 GB
	sda: [/] 38 %, 45.1/119 GB
	wlp1s0: 4 | 3 kbit/s

## Usage

	cnsstat [NETDEV] ...

Specify a list of network devices to display on the command
line, any that are up will be included in the output.

## Requirements

   - psutil

## Installation

	$ python3 -m venv --system-site-packages venv
	$ ./venv/bin/pip install cnsstat

