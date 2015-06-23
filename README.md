
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

#### Running

    opus20_cli 192.168.1.55 get 0x0064
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

