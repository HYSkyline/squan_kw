# -*- coding:utf-8 -*-

import time
import asyncio
import nest_asyncio

nest_asyncio.apply()
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

global time_start
WORKING_DIR = "./local01"
time_start = time.time()
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="qwq",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        llm_model_kwargs={
            "host": "http://localhost:11434",
            "options": {"num_ctx": 32768},
        },
        embedding_func=EmbeddingFunc(
            embedding_dim=1024,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model="bge-m3", host="http://localhost:11434"
            ),
        ),
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


def cont_read(f_input_path):
    cont = []
    with open(f_input_path, 'r', encoding='utf-8') as f_input:
        for each in f_input.readlines():
            cont.append(each[:-1])
    return cont


def main(modes, question):
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())

    # Insert example text
    rag.insert(cont_read('./book.txt'))

    # Test different query modes
    for mode in modes:
        print(f'\n使用{mode}模式的查询结果:')
        print(rag.query(question, param=QueryParam(mode=mode)))
    print(u'总计用时:' + str(time.time() - time_start) + 's.')

    # stream response
    # resp = rag.query(
    #     u"用简短的语言告诉我，如果我看到校长进入食堂就餐，我该怎么办?",
    #     param=QueryParam(mode="hybrid", stream=True),
    # )

    # if inspect.isasyncgen(resp):
    #     asyncio.run(print_stream(resp))
    # else:
    #     print(resp)


if __name__ == "__main__":
    modes = ['naive', 'local', 'global', 'hybrid']
    question = u"用简短的语言告诉我，如果我看到校长进入食堂就餐，我该怎么办?"
    main(modes, question)
