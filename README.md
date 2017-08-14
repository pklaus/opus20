
### opus20 - a Python interface to the OPUS20

This is a *opus20*, a Python software to query the temperature / 
humidity / air pressure logging device OPUS20 produced by Lufft.

#### Requirements

*opus20* depends (only) on Python version 3.3+.
I thought about backporting it to Python 2.7+ but it's not done so far.

The web interface requires a couple of Python packages:

    pip install jinja2 bottle matplotlib pandas numpy

Installing matplotlib may also require you to install
the python development package (for Python 3).

#### Installing

This package can be installed via pip:

    pip install --upgrade https://github.com/pklaus/opus20/archive/master.zip

To install all requirements for the included plot web server, too, run this command instead:

    pip install --upgrade https://github.com/pklaus/opus20/archive/master.zip#egg=opus20[webserver]

#### Usage

The Python package installs a command line tool to query the device
for current values. It's called `opus20_cli`.

Here is how to get a list of all available *channels* from the device:

    philipp@lion:~> opus20_cli 192.168.1.55 list
    Channel   100 (0x0064): CUR temperature         unit: °C    offset: ±10.0  logging: no
    Channel   120 (0x0078): MIN temperature         unit: °C    offset: ±10.0  logging: no
    Channel   140 (0x008C): MAX temperature         unit: °C    offset: ±10.0  logging: no
    Channel   160 (0x00A0): AVG temperature         unit: °C    offset: ±10.0  logging: yes
    Channel   105 (0x0069): CUR temperature         unit: °F    offset: 0.0    logging: no
    Channel   125 (0x007D): MIN temperature         unit: °F    offset: 0.0    logging: no
    Channel   145 (0x0091): MAX temperature         unit: °F    offset: 0.0    logging: no
    Channel   165 (0x00A5): AVG temperature         unit: °F    offset: 0.0    logging: no
    Channel   200 (0x00C8): CUR relative humidity   unit: %     offset: ±30.0  logging: no
    Channel   220 (0x00DC): MIN relative humidity   unit: %     offset: ±30.0  logging: no
    Channel   240 (0x00F0): MAX relative humidity   unit: %     offset: ±30.0  logging: no
    Channel   260 (0x0104): AVG relative humidity   unit: %     offset: ±30.0  logging: yes
    Channel   205 (0x00CD): CUR absolute humidity   unit: g/m³  offset: 0.0    logging: no
    Channel   225 (0x00E1): MIN absolute humidity   unit: g/m³  offset: 0.0    logging: no
    Channel   245 (0x00F5): MAX absolute humidity   unit: g/m³  offset: 0.0    logging: no
    Channel   265 (0x0109): AVG absolute humidity   unit: g/m³  offset: 0.0    logging: yes
    Channel   110 (0x006E): CUR dewpoint            unit: °C    offset: 0.0    logging: no
    Channel   130 (0x0082): MIN dewpoint            unit: °C    offset: 0.0    logging: no
    Channel   150 (0x0096): MAX dewpoint            unit: °C    offset: 0.0    logging: no
    Channel   170 (0x00AA): AVG dewpoint            unit: °C    offset: 0.0    logging: yes
    Channel   115 (0x0073): CUR dewpoint            unit: °F    offset: 0.0    logging: no
    Channel   135 (0x0087): MIN dewpoint            unit: °F    offset: 0.0    logging: no
    Channel   155 (0x009B): MAX dewpoint            unit: °F    offset: 0.0    logging: no
    Channel   175 (0x00AF): AVG dewpoint            unit: °F    offset: 0.0    logging: no
    Channel 10020 (0x2724): CUR battery voltage     unit: V     offset: 0.0    logging: no
    Channel 10040 (0x2738): MIN battery voltage     unit: V     offset: 0.0    logging: no
    Channel 10060 (0x274C): MAX battery voltage     unit: V     offset: 0.0    logging: no
    Channel 10080 (0x2760): AVG battery voltage     unit: V     offset: 0.0    logging: yes


Asking for the value of a channel works like this:

    philipp@lion:~> opus20_cli 192.168.1.55 get 0x0064
    24.712

You can also download the values stored on the device and store them in a file:

    philipp@lion:~> opus20_cli --loglevel INFO 192.168.1.55 download log_data.pickle
    INFO:opus20.opus20:Connected to device with ID: EC9C0A06B183
    INFO:opus_cli:script running time (net): 1.208517 seconds.
    philipp@lion:~>

Here is an overview of all the possible CLI commands:

    # List all possible channels:
    opus20_cli 192.168.1.55 list

    # Get the values for the specified channels (CUR, MIN, MAX temperature in °C):
    opus20_cli 192.168.1.55 get 0x0064 0x0078 0x008C

    # Download the latest log data and merge it into a persistant data file:
    opus20_cli 192.168.1.55 download opus20.PickleStore.p

    # Check if logging in general is enabled on the device:
    opus20_cli 192.168.1.55 logging status
    opus20_cli 192.168.1.55 logging start
    opus20_cli 192.168.1.55 logging stop
    # Or clear the log:
    opus20_cli 192.168.1.55 logging clear

    # Enable or disable logging for individual channels:
    opus20_cli 192.168.1.55 enable  0x0064 0x0078 0x008C
    opus20_cli 192.168.1.55 disable 0x00CD 0x00E1 0x00F5

#### Author

* (c) 2015, Philipp Klaus  
  <klaus@physik.uni-frankfurt.de>  
  Ported the software to Python, extended and packaged it.
* (c) 2012, [Ondics GmbH](http://www.ondics.de)  
  <githubler@ondics.de>  
  The author of the [original scripts][l2p_bash_scripts] (written as Bash scripts + netcat & gawk)

#### License

GPLv3

[l2p_bash_scripts]: https://github.com/ondics/lufft-l2p-script-collection

