import openai
import os.path
from colorama import Fore, init
import time

prompt = 'You: \nAI: \n'
prompt_sim = ''


def create_competitions(pre):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=pre,
        temperature=0.9,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" You:", " AI:"]
    )
    message = response.choices[0].text
    k = 0
    for i in range(len(message)):
        if message[i] != '\n':
            k = i
            break
    message = message[k:len(message)]
    return message


def create_competitions_sim(pre):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=pre,
        temperature=0.9,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    message = response.choices[0].text
    k = 0
    for i in range(len(message)):
        if message[i] != '\n' and message[i + 1] != '\n':
            k = i
            break
    message = message[k:len(message)]
    return message


def key_validity_cheak(key):
    if (key[0:3] != 'sk-'):
        return False
    if len(key) != 51:
        return False
    return True


def create_record_filename():
    time_tuple = time.localtime(time.time())
    # current_year = str(time_tuple[0])
    current_month = str(time_tuple[1])
    current_day = str(time_tuple[2]).zfill(2)
    current_hour = str(time_tuple[3]).zfill(2)
    current_minute = str(time_tuple[4]).zfill(2)
    current_second = str(time_tuple[5]).zfill(2)
    filename = '{}月{}日-{}时{}分{}秒.txt'.format(current_month, current_day, current_hour, current_minute,
                                                  current_second)
    return filename


def record_text(ht, at, filename):
    # if not (os.path.isdir('./record')):
    #     os.mkdir('./record')
    # with open('./record/{}'.format(filename), 'w', encoding='utf-8') as F:
    #     F.write(text)
    if not (os.path.isdir('./record')):
        os.mkdir('./record')
    with open('./record/{}'.format(filename), 'a', encoding='utf-8') as F:
        F.write('You: {}\n{}\n'.format(ht, at))


def record_text_sim(ht, at, filename):
    if not (os.path.isdir('./record')):
        os.mkdir('./record')
    # if not (os.path.isfile('./record/{}'.format(filename))):
    #     os.system('type nul > {}'.format(filename))
    with open('./record/{}'.format(filename), 'a', encoding='utf-8') as F:
        F.write('You: {}\nAI: {}\n'.format(ht, at))


def verify() -> str:  # API Key验证以及输入保存
    if not (os.path.isfile('./key.txt')):
        os.system('type nul > key.txt')
    with open('key.txt', 'r+') as F:
        key = F.readline()
        F.seek(0)  # 指针归位到文件开头
        F.truncate()  # 指针以后的全部删除
        if len(key) == 0:
            key = input(Fore.RED + '未识别到存在的API key，请手动输入API key\n')
        while (True):
            flag = key_validity_cheak(key)
            if not flag:
                key = input(Fore.RED + '当前API Key无效，请重新输入API Key\n')
            else:
                F.write(key)
                return key


if __name__ == '__main__':

    init()
    openai.api_key = verify()
    operation = int(input(
        Fore.YELLOW + '若你想要对话实现上下文关联，请输入1，否则输入2\n(注意:上下文关联所消耗的资源随着对话进行呈指数级增长)\n'))
    while not (operation == 1 or operation == 2):
        operation = int(input('无效的数字，请重新输入\n'))

    filename = create_record_filename()

    if operation == 1:
        while (True):
            query = input(Fore.WHITE + 'You: ')
            prompt = '{}You: {}\n'.format(prompt, query)
            message = create_competitions(prompt)
            prompt = '{}{}\n'.format(prompt, message)
            print('{}\n'.format(message))
            record_text(query, message, filename=filename)



    elif operation == 2:
        while (True):
            query = input(Fore.WHITE + 'You: ')
            human_text_sim = query
            message = create_competitions_sim(query)
            ai_text_sim = message
            print('AI: {}\n'.format(message))
            record_text_sim(human_text_sim, ai_text_sim, filename=filename)
