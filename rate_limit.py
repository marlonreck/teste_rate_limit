#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:43:25 2023

@author: Marlon V. Reck
e-mail: marlon.reck@cresol.coop.br
Linkedin: https://br.linkedin.com/in/marlonreck

Version: 0.1
Description: Teste de rate limits
Requirement: aiohttp asyncio time datetime nest_asyncio argparse
"""

import aiohttp
import asyncio
import time
import datetime
import nest_asyncio
import argparse

nest_asyncio.apply()

'''
Por design, o asyncio não permite que seu loop de eventos seja aninhado.
Isso apresenta um problema prático: quando em um ambiente em que o loop de 
eventos já está em execução, é impossível executar tarefas e aguardar o 
resultado.
Tentar fazer isso dará o erro:
    “RuntimeError: Este loop de eventos já está em execução”.

O problema aparece em vários ambientes, como servidores da Web, 
aplicativos GUI e em notebooks Jupyter.
Este módulo corrige o asyncio para permitir o uso aninhado de asyncio.run 
e loop.run_until_complete.
'''

start_time = time.time()

async def resp_status(session, url):
    atual = datetime.datetime.now().strftime("%H:%M:%S:%f")
    async with session.get(url, ssl=False) as resp:
        return (resp.status, atual)

async def get_url(url,n):
    async with aiohttp.ClientSession() as session:
        r_ok = 0
        r_erro = 0
        tasks = []
        for numero in range(n):
            tasks.append(asyncio.ensure_future(resp_status(session, url)))

        ret_tasks = await asyncio.gather(*tasks)
        for item in ret_tasks:
            print(f"{ret_tasks.index(item)} {url} {item}")
            if item[0] == 200:
                r_ok += 1
            else:
                r_erro += 1
        print("--- %s seconds ---" % (time.time() - start_time))
        print(f'\nRequisições aceitas {r_ok}')
        print(f'Requisições bloqueadas {r_erro} \n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description='Teste de rate limit/DDOS')
    parser.add_argument('-u', '--url', dest= 'url', action = 'store',
                        required = True,
                        help = 'Informe a url ou o ip para o teste.')
    parser.add_argument('-r', '--request', dest='request', action = 'store',
                        type=int, default=1, required = True,
                        help = 'Informe o número de requisições que será feita.')
    
    argumento = parser.parse_args()
    asyncio.run(get_url(argumento.url, argumento.request))
