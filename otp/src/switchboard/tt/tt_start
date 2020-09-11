#!/bin/bash

SBPATH="/sbpub/otp/switchboard"
TTPATH="/sbpub/otp/switchboard/tt"

pushd . 2>&1 > /dev/null

cd $TTPATH
python ../startNode.py --name TTGREG --nodeport 6123 --nshost localhost --nsport 6053 --clhost vrops73.starwave.com --clport 6060 --dshost dnhspapp03.online.disney.com --dsport 9005 >> node.TTGREG.log 2>&1 &

sleep 5
python ../startNode.py --name TTJOHN --nodeport 6124 --nshost localhost --nsport 6053 --clhost vrops73.starwave.com --clport 6060 --dshost dnhspapp03.online.disney.com --dsport 9005 >> node.TTJOHN.log 2>&1 &

sleep 5
python ../startNode.py --name TTRED  --nodeport 6125 --nshost localhost --nsport 6053 --clhost vrops73.starwave.com --clport 6060 --dshost dnhspapp03.online.disney.com --dsport 9005 >> node.TTRED.log 2>&1 &

sleep 5
python ../startNode.py --name TTIAN  --nodeport 6126 --nshost localhost --nsport 6053 --clhost vrops73.starwave.com --clport 6060 --dshost dnhspapp03.online.disney.com --dsport 9005 >> node.TTIAN.log 2>&1 &

popd
