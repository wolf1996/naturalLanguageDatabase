#!/bin/bash
#/home/ksg/disk_d/labs_2017/diploma/syntaxnet/models/syntaxnet
#/home/ksg/disk_d/labs_2017/diploma/pretrained_model/Russian
cd $1
MODEL_DIRECTORY=$2
echo $3 |syntaxnet/models/parsey_universal/parse.sh \
    $MODEL_DIRECTORY