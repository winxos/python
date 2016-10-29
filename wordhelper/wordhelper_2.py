# -*- coding: utf-8 -*-
'''
带限制构词游戏
寻找只用特定字母构成的单词
词库可以根据自己喜好扩充
winxos 2012-9-27
'''
words={}
sp='yaomingtekfc'
#lambda函数定义，核心算法
#得到最大长度
maxwordlen=lambda words:max(map(lambda x:len(x),words.keys()))
#得到长度大于某数的单词
maxword=lambda words,l:filter(lambda x:len(x)>=l,words.keys())
#判断一个单词是否符合要求
isvalide = lambda word,s:len(filter(lambda x:s.find(x)<0,word))==0
#寻找全部符合条件单词
filterwords = lambda words,c:filter(lambda x:isvalide(x,c),words.keys())

#装载常用词汇
def loadwords(name):
    global words
    d=open(name).read().split('\n')
    for line in d:
        if(len(line)==0):continue
        w=line.split()[0]
        words[w]=line[len(w):]
if __name__ == '__main__':
    loadwords('E:\skydrive\我的程序\Py\wordhelper\8000.txt')
    print '常用词库大小:',len(words)
    ans=filterwords(words,sp)
    ans.sort()
    print '测试条件:',sp,'\n符合条件单词数目:',len(ans)
    print ','.join(ans)



