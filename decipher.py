import json
import re
from collections import Counter
import os

def Creat_dict(input_dict,text):
    letter_dict = {} 
    for letter in range (0,26):
        letter_dict[chr(letter+97)] = 0
    message = text
    for i in message:
        if('a'<=i<='z'):
            letter_dict[i] = letter_dict[i] + 1
    for key in list(input_dict.keys()):
        letter_dict[key] = input_dict[key]
    return letter_dict

def initialize_dict_status(input_dict):
    dict_status = {}
    for letter in range (0,26):
        dict_status[chr(letter+97)] = 0
    for key in list(input_dict.keys()):
        dict_status[key] = 1
    return dict_status

def deciphering(letter_dict,text):
    message = text
    str = ''
    for i in message:
        if('a'<=i<='z'):
            str = str + letter_dict[i]
        else:
            str = str + i
    return str

def combine(letter_dict,word1,word2):
    for i in range(len(word1)):
        if (type(letter_dict[word1[i]]) == str and letter_dict[word1[i]] != word2[i]):
            return False,letter_dict
        key = get_key(letter_dict,word2[i])
        if len(key) != 0 and letter_dict[word1[i]] != word2[i]:
            return False,letter_dict
    for i in range(len(word1)):
        letter_dict[word1[i]] = word2[i]
    return True,letter_dict

def word_pair(letter_dict,words,level):
    for word2 in level:
        for word1 in list(words[len(word2)].keys()):
            status,letter_dict = combine(letter_dict,word1,word2)
            if status:
                break
    return letter_dict

def Word_Frequecy(letter_dict,text):
    message = text
    message = re.sub(r'[\W,\s]',' ',message)
    word = message.split()
    words = {}
    for w in word:
        if len(w) not in words:
            words[len(w)] = []
        words[len(w)].append(w)
    for key in words:
        words[key] = sorted(dict(Counter(words[key])).items(),key=lambda d: d[1], reverse=True)
        words[key] = {key: value for key, value in words[key]} 
    level = ['a','the','which','of','and','to','for']
    letter_dict = word_pair(letter_dict,words,level)
    return letter_dict

def Letter_Frequecy(letter_dict):
    path = re.sub(r'\\','/',os.getcwd()) +'/save.json'
    with open(path,"r",encoding='utf-8') as f:
        load_dict = json.load(f)
    load_dict = dict(sorted(load_dict.items(),key=lambda d: d[1], reverse=True))
    dic = {}
    for key in letter_dict:
        if type(letter_dict[key]) == int:
            dic[key] = letter_dict[key]
        else:
            del load_dict[letter_dict[key]]
    dic = dict(sorted(dic.items(),key = lambda d:d[1],reverse=True))
    for key in dic:
        letter_dict[key] = list(load_dict.keys())[0]
        del load_dict[list(load_dict.keys())[0]]
    return letter_dict

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

def change (letter_dict,a,b):
    if len(get_key(letter_dict,b)) != 0 and len(a) == 1:
        letter_dict[get_key(letter_dict,b)[0]] = letter_dict[a]
        letter_dict[a] = b
    return letter_dict

def Get_Message(letter_dict,text):
    message = text
    message = re.sub(r'[\W,\s]',' ',message)
    word = message.split()
    words = {}
    for key in word:
        words[key] = word_decipher(key,letter_dict)
    return words

def get_status(words,dict_status):
    for key in list(words.keys()):
        if known(words[key]):
            for letter in key:
                dict_status[letter] = 1
            del words[key]
    return dict_status

def get(words,dict_status,num):
    for key in list(words.keys()):
        if len(key) < num:
            del words[key]
    return get_status(words,dict_status)

def Add_Input_Dict(input_dict):
    key = input()
    value = input()
    if len(key) == 1 and len(value) == 1:
        input_dict[key] = value
    else:
        print('Input Error')
    return input_dict

def Delet_Input_Dict(input_dict):
    word = input()
    for key in list(input_dict.keys()):
        if key == word:
            del input_dict[word]
            return input_dict
    print('None')
    return input_dict

path = re.sub(r'\\','/',os.getcwd()) +'/dict.txt'
with open(path,'r') as f:
    words = re.findall("[a-z]+", f.read().lower())
word_counts = Counter(words)

def known(word):
    if word in word_counts:
        return True
    return False

def splits(word):# 分割单词
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

def edits(key,word,letter_dict,dict_status):
    alphabet = ''.join([chr(ord('a') + i) for i in range(26)])
    replaces = []
    edit_words = []
    for letter in dict_status.keys():
        if dict_status[letter] == 1:
            alphabet = re.sub(letter_dict[letter],'',alphabet)
    for num in range(len(word)):#查找只需要替换一个字符的
        if dict_status[key[num]] == 0:
            for letter in alphabet:
                replaces.append(word[:num] + letter + word[num+1:])
    for key in replaces:
        if known(key):
            edit_words.append(key)
    if len(edit_words) > 0:
        edit_word = max(edit_words,key=word_counts.get)
        for num in range(len(word)):
            if word[num] != edit_word[num]:  
                letter_dict = swap(letter_dict,word[num],edit_word[num])
                dict_status[dict_index(letter_dict,edit_word[num])] = 1
    return letter_dict,dict_status

def dict_index(dict,value):
    return list(dict.keys())[list(dict.values()).index(value)]

def swap(letetr_dict,a,b):
    tempa = dict_index(letetr_dict,a)
    tempb = dict_index(letetr_dict,b)
    letetr_dict[tempa] = b
    letetr_dict[tempb] = a
    return letetr_dict

def correct(key,word,letter_dict,dict_status):
    if known(word):
        return letter_dict,dict_status
    else:
        letter_dict,dict_status = edits(key,word,letter_dict,dict_status)
        return letter_dict,dict_status

def word_decipher(key,letter_dict):
    str = ''
    for num in range(len(key)):
        str = str + letter_dict[key[num]]
    return str

def Correct(letter_dict,dict_status,text):
    message = text
    row_words = re.sub(r'[\W,\s]',' ',message).split()
    for key in row_words:
        if len(key) > 3:
            letter_dict,dict_status = correct(key,word_decipher(key,letter_dict),letter_dict,dict_status)
    return letter_dict,dict_status

def decipher (text,commad,input_dict):
    letter_dict = Creat_dict(input_dict,text)
    if commad == 1:
        letter_dict = Word_Frequecy(letter_dict,text)
        letter_dict = Letter_Frequecy(letter_dict)
    if commad == 2:
        letter_dict = Word_Frequecy(letter_dict,text)
        letter_dict = Letter_Frequecy(letter_dict)
        for num in range(5):
            dict_status = initialize_dict_status(input_dict)
            dict_status = get(Get_Message(letter_dict,text),dict_status,5-num)
            letter_dict,dict_status = Correct(letter_dict,dict_status,text)
    message = deciphering(letter_dict,text)
    for key in list(input_dict.keys()):
        letter_dict[key] = letter_dict[key] + '*'
    return message,re.sub(r'[{} \' 0]','',re.sub(',','\n',str(letter_dict)))
    if commad == 3:
        input_dict = Add_Input_Dict(input_dict)
    if commad == 4:
        input_dict = Delet_Input_Dict(input_dict)

# if __name__ == '__main__':
#     path = re.sub(r'\\','/',os.getcwd()) +'/c.txt'
#     f=open(path,"r",encoding = "utf-8")
#     text = f.read()
#     decipher(text,2)