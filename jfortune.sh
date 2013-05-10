#!/bin/bash
wget -q -O - http://www.meigensyu.com/quotations/view/random | grep "class=\"text\"" | sed -e 's/<[^>]*>//g'
