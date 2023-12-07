# Natural Language to SQL: Fine-Tuning CodeLlama with Amazon SageMaker - Part 1

## Overview

This repository contains resources and guides from the blog series "Natural Language to SQL: Fine-Tuning CodeLLama with Amazon SageMaker". The first part introduces the concept of NL2SQL, the role of large language models (LLMs) like CodeLLama in this domain, and practical strategies for fine-tuning these models using Quantized Low-Rank Adaptation (QLoRA) on Amazon SageMaker.

## Getting started

1/ Inspect `download_spider.sh`. It will download the dataset into a folder for you to use.

2/ Create a conda env from the `environment.yml` file.

2/ Run through the notebook `CodeLlama_fine_tuning.ipynb`

3/ Run the benchmark script with `python utils/benchmark.py`

## License

Code and notebooks are licensed under the [MIT](https://opensource.org/license/mit/) licence.

All derived work based on SPIDER Dataset [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode) licence.
