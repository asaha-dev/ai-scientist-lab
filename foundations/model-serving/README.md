## Model Serving

A hands on tutorial for running open-source models locally and serving them with modern inference engines. The goal is to learn how to take an open-source model, run it locally and expose it as a service for other applications to use it. 

### Reading materials
https://huggingface.co/docs/transformers/pipeline_tutorial
https://huggingface.co/docs/transformers/en/community_integrations/vllm


### What I will cover
* a causal language model for text generation
* an embedding model for vector representations
* a reasoning-capable language model
* local inference with HF transformers
* an http model API 
* vLLM/SGLang/TensorRT-LLM
* basic benchmarking like latency and throughput

### Mental model

The central idea is to separate 3 concepts: 

MODEL -- the learned neural network and its weights.
RUNTIME / INFERENCE ENGINE -- software that executes the model efficiently 
SERVER -- A long running process that exposes the interface through an API. 

For example, local run: 
Model repo --> download tokenizer + config + model weights --> inference framework --> CPU/GPU --> Model generates tokens.

When serving: 
Client --> http request --> Inference server --> Tokenizer --> Model --> CPU/GPU --> Http response


