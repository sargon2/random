#!/bin/bash
echo -n "VFINX: $";
curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=VFINX&f=l1'

echo -n "NASDAQ:EDS: $";
curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=eds&f=l1'

echo -n "HPQ: $";
curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=hpq&f=l1'

echo -n "Bitcoin: ";
#curl -s 'https://mtgox.com/api/0/data/ticker.php'
curl -s 'https://mtgox.com/api/1/BTCUSD/ticker' | tr '}' '\n' | grep last\" | grep -o "\"display\":\"[^\"]\+" | cut -c 12-
