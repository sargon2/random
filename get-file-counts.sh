#!/bin/bash -e

for i in *; do echo -n "$i: "; find "$i" | wc -l; done | sort -t ":" -k2 -n
