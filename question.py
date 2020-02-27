import os
import pdb

from bs4 import BeautifulSoup
import requests

username = '丰赵'
base_url = 'https://zhidao.baidu.com'

def process_question_from_str(st):
    soup = BeautifulSoup(st)
    if soup.title.text.find('信息提示') > 0:
        return 'deleted'

    # whether I am the best replier
    repliers = soup.find_all(class_='wgt-replyer-all-card')
    # find my replier index    
    index = 0
    for i in repliers:
        if i.text.find(username) > 0:
            break
        index += 1
    if index == 0:
        my_answer = soup.find(class_='best-text')
        if my_answer is None:
            my_answer = soup.find(class_='answer-text')
    else:
        index -= 1
        my_answer = soup.find_all(class_='answer-text')[index]
    try:
        my_answer_text = my_answer.text.replace('展开全部','')
    except:
        pdb.set_trace()
    my_answer_text = my_answer_text.replace('\n\n\n','')
    try:
        question = soup.find(class_='q-content').find_all('span')[1]
    except Exception as e:
        # account deleted, use title instead
        question = soup.find('title')
    question_text = question.text.rstrip('_百度知道')

    return question_text + '\n\n' + my_answer_text

def process_question_from_file(file_name):
    with open(file_name) as f:
        st = f.read()
    return process_question_from_str(st)
 
def process_question_from_url(url):
    question_id = url.split('/')[-1]
    file_name = os.path.join('build', question_id + '.html')
    if not os.path.exists(file_name):
        whole_url = base_url + url
        r = requests.get(whole_url)
        if r.status_code != 200:
            pdb.set_trace()
        r.encoding = 'gbk'
        with open(file_name, 'w') as f:
            f.write(r.text)
    return process_question_from_file(file_name)
    
