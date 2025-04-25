from openai import OpenAI
from datetime import datetime
import json
import os
import requests

from wheel.wheel_test import calc_slide_time

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-e05b2740746f4c14ae025425b06acec5",
    base_url="https://api.deepseek.com",  # 填写DashScope SDK的base_url
)

# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {  
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    },
    # 工具3 获取飞轮惯滑时间
    {
        "type": "function",
        "function": {
            "name": "calc_slide_time",
            "description": "当你想查询和计算飞轮惯滑时间非常有用。",
            "parameters": {  
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "北京时间, 格式为: 2025-02-15T09:10:00"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "北京时间, 格式为: 2025-02-15T09:30:00"
                    },
                    "sat_name": {
                        "type": "string",
                        "description": "卫星名称，只能在 a02, b01, b02, b03 四种类型中选择"
                    },
                    "wheel_list": {
                        "type": "array",
                        "description": "飞轮编号列表，默认为['A','B','C','D']"
                    }
                }
            },
            "required": [
                "start_time",
                "end_time",
                "sat_name",
                "wheel_list"
            ]
        }
    },
]

# 模拟天气查询工具。返回结果示例：“北京今天是雨天。”
def get_current_weather(location):
    return f"{location}今天是雨天。 "

# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

# 封装模型响应函数
def get_response(messages):
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="required"
        )
    return completion.model_dump()

def function_call_2():
    messages = []
    while True:
        messages.append({"role": "user", "content": input()})

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )

        print(response.choices[0].message)
        messages.append(response.choices[0].message)

        print(messages)


        if response.choices[0].message.tool_calls is not None and response.choices[0].message.content is None:
            tool_call = response.choices[0].message.tool_calls[0]

            if tool_call.function.name == 'calc_slide_time':
                tool_info = {"name": "calc_slide_time", "role":"tool"}
                # 提取参数信息
                arguments = json.loads(tool_call.function.arguments)
                start_time = arguments['start_time']
                end_time = arguments['end_time']
                sat_name = arguments['sat_name']
                wheel_list = arguments['wheel_list']
                tool_info['content'] = calc_slide_time(start_time, end_time, sat_name, wheel_list)


def call_with_messages():
    print('\n')
    messages = [
            {
                "content": input('请输入：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
                "role": "user"
            }
    ]
    print("-"*60)

    # 模型的第一轮调用
    i = 1
    first_response = get_response(messages)
    assistant_output = first_response['choices'][0]['message']
    print(f"\n第{i}轮大模型输出信息：{first_response}\n")
    if  assistant_output['content'] is None:
        assistant_output['content'] = ""
    messages.append(assistant_output)
    # 如果不需要调用工具，则直接返回最终答案
    if assistant_output['function_call'] is None:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
        print(f"{assistant_output['content']}")
        return False
    
    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while assistant_output['tool_calls'] != None:
        # 如果判断需要调用查询天气工具，则运行查询天气工具
        if assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
            tool_info = {"name": "get_current_weather", "role":"tool"}
            # 提取位置参数信息
            location = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
            tool_info['content'] = get_current_weather(location)
        # 如果判断需要调用查询时间工具，则运行查询时间工具
        elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
            tool_info = {"name": "get_current_time", "role":"tool"}
            tool_info['content'] = get_current_time()
        elif assistant_output['tool_calls'][0]['function']['name'] == 'calc_slide_time':
            tool_info = {"name": "calc_slide_time", "role":"tool"}
            # 提取参数信息
            arguments = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])
            start_time = arguments['start_time']
            end_time = arguments['end_time']
            sat_name = arguments['sat_name']
            wheel_list = arguments['wheel_list']
            tool_info['content'] = calc_slide_time(start_time, end_time, sat_name, wheel_list)
            
        # print(f"工具输出信息：{tool_info['content']}\n")
        print("-"*60)
        messages.append(tool_info)
        assistant_output = get_response(messages)['choices'][0]['message']
        if  assistant_output['content'] is None:
            assistant_output['content'] = ""
        messages.append(assistant_output)
        i += 1
        # print(f"第{i}轮大模型输出信息：{assistant_output}\n")
    print(f"最终答案：{assistant_output['content']}")
    return True

def only_chat():

    messages = []
    while True:
        messages.append({"role": "user", "content": input()})

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )

        print(response.choices[0].message.content)

        messages.append(response.choices[0].message)



def function_call():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather of an location, the user shoud supply a location first",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"]
                },
            }
        },
    ]

    messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )

    print(response.choices[0].message)

def get_token():
    url = "https://api.deepseek.com/user/balance"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer sk-e05b2740746f4c14ae025425b06acec5'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=10)

    print(response.text)


if __name__ == '__main__':
    # get_token()
    # only_chat()
    function_call_2()
    # while True:
    #     ret = call_with_messages()
    #     if ret:
    #         break
