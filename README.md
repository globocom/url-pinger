URL Pinger
==========

It pings a URL and follows redirects, and report FAIL or SUCCESS. That's it.


How to Use
----------

    $ git clone https://github.com/globocom/url-pinger.git
    $ cd url-pinger
    $ pip install -r requirements.txt
    $ echo http://www.globo.com > public_sites.txt
    $ export SITES_TXT=public_sites.txt
    $ python pinger.py &
    $ open http://localhost:5000


Sites.txt Format
----------------

    protocol://url1
    protocol://url2 user:password

See https://raw.github.com/globocom/url-pinger/master/sites.txt