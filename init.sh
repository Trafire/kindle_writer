#!/bin/sh

pip install -q git+https://github.com/huggingface/transformers.git
pip install google-cloud-storage
export XRT_TPU_CONFIG="localservice;0;localhost:51011"

