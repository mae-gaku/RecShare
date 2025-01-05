## How to Uses
```
wget https://huggingface.co/localmodels/Llama-2-7B-Chat-ggml/resolve/main/llama-2-7b-chat.ggmlv3.q2_K.bin
```

Llama3.2 1B
```
https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-f16.gguf
```

```
git clone https://github.com/ggerganov/llama.cpp.git
```
```
cd llama.cpp
```

### Convert
```
python3 convert_llama_ggml_to_gguf.py --input ../llama-2-7b-chat.ggmlv3.q2_K.bin --output llama-model.gguf
```

### Docker
```
docker build -t llama .
```

```
docker run -it -v /home/gaku/github/Technical_Tools/LLM/llama_app/:/mnt llama /bin/bash

```

```
python3 -m pip install python-dotenv
```

```
streamlit run app.py
```


```
streamlit run app.py --server.fileWatcherType none
```


※VMの設定で仮想環境支援がONになっているとうまくいかない