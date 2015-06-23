
### Lufft Opus20

This is a Python software to query the
temperature/humidity/... measurement device
Opus20 produced by Lufft.

#### Installing

*lufft_opus20* can be installed via pip:

    pip install --upgrade .

#### Running

    opus20_cli 192.168.1.55 get 0x0064
    24.712

#### Author

* (c) 2015, Philipp Klaus  
  <klaus@physik.uni-frankfurt.de>  
  Ported the software to Python, extended and packaged it.
* (c) 2012, [Ondics GmbH](http://www.ondics.de)  
  <githubler@ondics.de>  
  The author of the [original scripts][] (written as Bash scripts + netcat & gawk)

#### License

GPLv3

[original_scripts]: https://github.com/ondics/lufft-l2p-script-collection

