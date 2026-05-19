#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
netconvert \
  --node-files plain/east_sarajevo_test.nod.xml \
  --edge-files plain/east_sarajevo_test.edg.xml \
  --connection-files plain/east_sarajevo_test.con.xml \
  --output-file east_sarajevo_test.net.xml

echo "Built 2_network/east_sarajevo_test.net.xml"
