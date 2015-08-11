#!/bin/bash

STOCKS=vfinx,vbk,hpq

curl -s "http://finance.google.com/finance/info?q=$STOCKS" | egrep "\"t\"|\"l_fix\"" | paste -s -d' \n' | sed 's/,\"t\" : //' | sed 's/ ,\"l_fix\" : /: \$/' | tr -d '\"'
