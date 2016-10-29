#coding=utf-8
'''
带限制构词游戏
寻找只用特定字母构成的单词
词库可以根据自己喜好扩充
Python3 android版
winxos 2012-9-27
'''
words={}
sp='abcdefghijklmnopqrstuvwxyz'
#lambda函数定义，核心算法
#得到最大长度
maxwordlen=lambda words:max(list(map(lambda x:len(x),words))) #python 2中map, filter直接返回列表
#得到长度大于某数的单词
maxword=lambda words,l:list(filter(lambda x:len(x)>=l,words))
#判断一个单词是否符合要求
isvalide = lambda word,s:len(list(filter(lambda x:s.find(x)<0,word)))==0
#寻找全部符合条件单词
filterwords = lambda words,c:list(filter(lambda x:isvalide(x,c),words))

#装载常用词汇
def loadwords(name):
    global words
    d=open(name).read().split('\n')
    for line in d:
        if(len(line)==0):continue
        w=line.split()[0]
        words[w]=line[len(w):]
if __name__ == '__main__':
    loadwords('scripts/ws/8000.txt')
    print ('总词库大小:',len(words))
    s=input('输入字母：')
    if s=='':s=sp
    ans=filterwords(words.keys(),s)
    ans.sort()
    print ('测试条件:',s,'\n符合条件单词数目:',len(ans))
    print (','.join(ans))



