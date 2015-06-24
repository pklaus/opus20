
### Lufft Opus20

This is a *lufft_opus20*, a Python software to query the
temperature/humidity/... measurement device
Opus20 produced by Lufft.

#### Requirements

*lufft_opus20* depends (only) on Python version 3.2+.
I thought about backporting it to Python 2.7+ but it's not done so far.

#### Installing

This package can be installed via pip:

    pip install --upgrade https://github.com/pklaus/lufft_opus20/archive/master.zip

#### Usage

The Python package installs a command line tool to query the device
for current values. It's called `opus20_cli`.

Here is how to get a list of all available *channels* from the device:

    philipp@lion:~> opus20_cli 192.168.1.55 list
    Channel   100 (0x0064): CUR temperature       min=-20.0  max=50.0   unit=°C   type=FLOAT offset=±10.0
    Channel   120 (0x0078): MIN temperature       min=-20.0  max=50.0   unit=°C   type=FLOAT offset=±10.0
    Channel   140 (0x008C): MAX temperature       min=-20.0  max=50.0   unit=°C   type=FLOAT offset=±10.0
    Channel   160 (0x00A0): AVG temperature       min=-20.0  max=50.0   unit=°C   type=FLOAT offset=±10.0
    Channel   105 (0x0069): CUR temperature       min=-4.0   max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   125 (0x007D): MIN temperature       min=-4.0   max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   145 (0x0091): MAX temperature       min=-4.0   max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   165 (0x00A5): AVG temperature       min=-4.0   max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   200 (0x00C8): CUR relative_humidity min=0.0    max=100.0  unit=%    type=FLOAT offset=±30.0
    Channel   220 (0x00DC): MIN relative_humidity min=0.0    max=100.0  unit=%    type=FLOAT offset=±30.0
    Channel   240 (0x00F0): MAX relative_humidity min=0.0    max=100.0  unit=%    type=FLOAT offset=±30.0
    Channel   260 (0x0104): AVG relative_humidity min=0.0    max=100.0  unit=%    type=FLOAT offset=±30.0
    Channel   205 (0x00CD): CUR absolute_humidity min=0.0    max=85.0   unit=g/m³ type=FLOAT offset=0.0
    Channel   225 (0x00E1): MIN absolute_humidity min=0.0    max=85.0   unit=g/m³ type=FLOAT offset=0.0
    Channel   245 (0x00F5): MAX absolute_humidity min=0.0    max=85.0   unit=g/m³ type=FLOAT offset=0.0
    Channel   265 (0x0109): AVG absolute_humidity min=0.0    max=85.0   unit=g/m³ type=FLOAT offset=0.0
    Channel   110 (0x006E): CUR dewpoint          min=-85.0  max=50.0   unit=°C   type=FLOAT offset=0.0
    Channel   130 (0x0082): MIN dewpoint          min=-85.0  max=50.0   unit=°C   type=FLOAT offset=0.0
    Channel   150 (0x0096): MAX dewpoint          min=-85.0  max=50.0   unit=°C   type=FLOAT offset=0.0
    Channel   170 (0x00AA): AVG dewpoint          min=-85.0  max=50.0   unit=°C   type=FLOAT offset=0.0
    Channel   115 (0x0073): CUR dewpoint          min=-121.0 max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   135 (0x0087): MIN dewpoint          min=-121.0 max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   155 (0x009B): MAX dewpoint          min=-121.0 max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel   175 (0x00AF): AVG dewpoint          min=-121.0 max=122.0  unit=°F   type=FLOAT offset=0.0
    Channel 10020 (0x2724): CUR battery voltage   min=0.0    max=6.5    unit=V    type=FLOAT offset=0.0
    Channel 10040 (0x2738): MIN battery voltage   min=0.0    max=6.5    unit=V    type=FLOAT offset=0.0
    Channel 10060 (0x274C): MAX battery voltage   min=0.0    max=6.5    unit=V    type=FLOAT offset=0.0
    Channel 10080 (0x2760): AVG battery voltage   min=0.0    max=6.5    unit=V    type=FLOAT offset=0.0

Asking for the value of a channel works like this:

    philipp@lion:~> opus20_cli 192.168.1.55 get 0x0064
    24.712

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

