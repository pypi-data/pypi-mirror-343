from openai import OpenAI
from mcp.client.sse import sse_client
from mcp import ClientSession
from contextlib import AsyncExitStack
import asyncio
import json


class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.deepseek = OpenAI(
            api_key='sk-a893b76d60e745a6bd5053cf1ca0e451',
            base_url='https://api.deepseek.com'
        )
        self.exit_stack = AsyncExitStack()

    async def run(self, query: str):
        # 改成用异步上下文堆栈来处理
        read_stream, write_stream = await self.exit_stack.enter_async_context(sse_client(self.server_url))
        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream=read_stream, write_stream=write_stream))

        # 4. 初始化通信
        await session.initialize()

        # 5. 获取服务端有的tools
        response = await session.list_tools()
        # print(response)

        # 6. 将工具封装Function Calling能识别的对象
        tools = []
        for tool in response.tools:
            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
            })

        # 7. 发送信息给大模型，让大模型自主选择调用哪个工具
        # role:
        #  1、user： 用户消息
        #  2、assistant： 大模型发送给用户的消息
        #  3、system： 给大模型的系统提示词
        #  4、tool： 函数执行完后返回的信息
        messages = [{
            "role": "user",
            "content": query
        }]

        deepseek_response = self.deepseek.chat.completions.create(
            model='deepseek-chat',
            messages=messages,
            tools=tools
        )
        # print(deepseek_response)

        choice = deepseek_response.choices[0]
        print('-----1---')
        print(choice)

        if choice.finish_reason == 'tool_calls':
            # 为了后期大模型能够更加精准的回复
            messages.append(choice.message.model_dump())

            print(choice.message.tool_calls)
            # 获取工具
            tool_calls = choice.message.tool_calls
            for tool_call in tool_calls:
                tool_id = tool_call.id
                function = tool_call.function
                function_name = function.name
                function_arguments = json.loads(function.arguments)

                result = await session.call_tool(function_name, arguments=function_arguments)
                # print(result)

                content = result.content[0].text
                messages.append({
                    "role": "tool",
                    "content": content,
                    "tool_call_id": tool_id
                })
        else:
            print('大模型没有找到合适的工具!')
            return

        resp = self.deepseek.chat.completions.create(
            model='deepseek-chat',
            messages=messages
        )
        print('-----2---')
        print(resp.choices[0].message.content)

    async def aclose(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPClient('http://127.0.0.1:8000/sse')
    try:
        await client.run('请帮查询select * from cdn_config.account_user中表的数据吧,因为我中sql中指名了数据库名，直接执行sql查询即可？')
    finally:
        await client.aclose()


if __name__ == '__main__':
    asyncio.run(main())





