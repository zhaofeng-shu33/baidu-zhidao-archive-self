import os
import pdb

from bs4 import BeautifulSoup
import requests
import shutil

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
    if index == len(repliers):
        return ''
    if index == 0:
        my_answer = soup.find(class_='best-text')
        if my_answer is None:
            my_answer = soup.find(class_='answer-text')
    else:
        index -= 1
        my_answer = soup.find_all(class_='answer-text')[index]
    my_answer_text = my_answer.text.replace('展开全部','')
    my_answer_text = my_answer_text.replace('\n\n\n','')
    try:
        question = soup.find(class_='q-content').find_all('span')[1]
    except Exception as e:
        # account deleted, use title instead
        question = soup.find('title')
    question_text = question.text.rstrip('_百度知道')
    try:
        question_img = soup.find(class_='q-img-ul').find('img')
        if question_img:
            img_url = question_img['src']
            img_name = img_url.split('/')[-1] + '.jpg'
            download_image(img_name, img_url)
            question_text += '\n![](%s)\n' % img_name
    except AttributeError:
        pass
    return question_text + '\n\n' + my_answer_text

def download_image(img_name, img_url):
    file_name = os.path.join('build', img_name)
    if not os.path.exists(file_name):
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print("Download for %s failed" % img_url)

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
    
