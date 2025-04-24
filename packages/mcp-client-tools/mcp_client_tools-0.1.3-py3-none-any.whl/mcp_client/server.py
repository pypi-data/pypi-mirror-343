from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
from async_exit_stack import AsyncExitStack
import pandas as pd
import json
import sys

class MCPClient:
    def __init__(self):
        self.write = None
        self.stdio = None
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self,env:dict|None,cmd :str, params: list) ->(str,str):
        server_params = StdioServerParameters(
            command=cmd,
            args=params,
            env=env
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        # 列出可用工具
        response = await self.session.list_tools()
        tools = response.tools

        retval:str = ""
        tlist: list = []
        for tool in tools:
            retval+="name="
            retval += tool.name
            tinfo = dict()
            tinfo['name'] = tool.name
            if tool.description is not None:
                retval += "\ndescription="
                retval += tool.description
                tinfo['description'] = tool.description
            retval += "\ninputSchema="
            retval += str(tool.inputSchema)
            tinfo['inputSchema'] = tool.inputSchema
            tlist.append(tinfo)
        return retval ,json.dumps(tlist,ensure_ascii=False)

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def run(env:dict |None, command: str, params :list)->str|None:
    print(f'command={command} params={params}')
    client = MCPClient()
    try:
        retval = await client.connect_to_server(env,command, params)
    finally:
        await client.cleanup()
    return retval


def build_env(keys :str) ->dict:
    env = dict()
    lines = keys.split('\n')
    for line in lines:
        values = line.split('=')
        if len(values) == 2:
            env[values[0]] = str(values[1])
    return env

def deal_csv_file(csv_file : str):
    data = pd.read_csv(csv_file)

    if 'tools' not in data.columns:
        data.insert(loc=len(data.columns), column='tools', value='')
    if 'json' not in data.columns:
        data.insert(loc=len(data.columns), column='json', value='')

    for index, row in data.iterrows():
        import time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(current_time)
        print(f'index {index}')
        param = row['params']

        if isinstance(param, str) and len(param) > 3:
           pass
        else:
            continue

        params = param.split('\n')
        args = row['args']

        if isinstance(args, str) and len(args) < 20:
            params.append(args.strip())

        keys = row['keys']
        value = row['tools']
        value_json = row['json']
        if isinstance(value, str) and len(value) > 10:
            print(value)
            print('-' * 100)
        else:
            if isinstance(keys, float) and len(row['command']) < 6:
                command = row['command']
                print(row['command'], params)
                value, value_json = asyncio.run(run(None, command, params))
            elif isinstance(keys, str) and len(row['command']) < 6:
                env = build_env(keys)
                command = row['command']
                print(row['command'], params)
                value, value_json = asyncio.run(run(env, command, params))
            data.loc[index, 'tools'] = value
            data.loc[index, 'json'] = value_json
            data.to_csv(csv_file)
            print(value)
            print('*' * 100)
    data.to_csv(csv_file)


def deal_xls_file(excel_file :str):
    data = pd.read_excel(excel_file)
    if 'tools' not in data.columns:
        data.insert(loc=len(data.columns), column='tools', value='')
    if 'json' not in data.columns:
        data.insert(loc=len(data.columns), column='json', value='')

    for index, row in data.iterrows():
        import time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(current_time)
        print(f'index {index}')
        param = row['params']

        if isinstance(param, str) and len(param) > 3:
           pass
        else:
            continue

        params = param.split('\n')
        args = row['args']

        if isinstance(args, str) and len(args) < 20:
            params.append(args.strip())

        keys = row['keys']
        value = row['tools']
        value_json = row['json']
        if isinstance(value, str) and len(value) > 10:
            print(value)
            print('-' * 100)
        else:
            if isinstance(keys, float) and len(row['command']) < 6:
                command = row['command']
                print(row['command'], params)
                value, value_json = asyncio.run(run(None, command, params))
            elif isinstance(keys, str) and len(row['command']) < 6:
                env = build_env(keys)
                command = row['command']
                print(row['command'], params)
                value, value_json = asyncio.run(run(env, command, params))
            data.loc[index, 'tools'] = value
            data.loc[index, 'json'] = value_json
            data.to_excel(excel_file)
            print(value)
            print('*' * 100)
    data.to_excel(excel_file)

def main():
    if len(sys.argv) < 2:
        print("Usage: uvx mcp-client-tools <path_to_cvs_file or path_xls_file contains columns keys, commands, params, args >")
        sys.exit(1)

    filename:str = sys.argv[1]
    if filename.lower().endswith(".csv"):
        deal_csv_file(filename)
    elif filename.lower().endswith("xls") or filename.lower().endswith("xlsx") :
        deal_xls_file(filename)
    else:
        print(f'不支持的文件格式！{filename}')
        sys.exit(1)


if __name__ == "__main__":
    main()