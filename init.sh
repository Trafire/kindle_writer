#!/bin/sh

pip3 install -q git+https://github.com/huggingface/transformers.git
pip3 install google-cloud-storage
export XRT_TPU_CONFIG="localservice;0;localhost:51011"
python3 main.py

