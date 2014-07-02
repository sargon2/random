#!/bin/bash

function display {
    # http://www.jarloo.com/yahoo_finance/
    echo -n "$1: $";
    curl -s "http://download.finance.yahoo.com/d/quotes.csv?s=$1&f=l1b3b2" | dos2unix | sed 's/,/ (/' | sed 's/,/ - /' | sed 's/$/)/g'
}


echo "stock: last price (bid - ask)"
display "VFINX"
display "EDS"
display "HPQ"
display "CAMP"

#echo -n "Bitcoin: ";
#curl -s 'https://mtgox.com/api/0/data/ticker.php'
#curl -s 'https://mtgox.com/api/1/BTCUSD/ticker' | tr '}' '\n' | grep last\" | grep -o "\"display\":\"[^\"]\+" | cut -c 12-
