# -*- coding: utf-8 -*-
'''
带限制构词游戏
寻找只用特定字母构成的单词
词库可以根据自己喜好扩充
winxos 2012-9-27
'''
words=[]
sp='yaomingtekfc'
#lambda函数定义，核心算法
#得到最大长度
maxwordlen=lambda words:max(map(lambda x:len(x),words))
#得到长度大于某数的单词
maxword=lambda words,l:filter(lambda x:len(x)>=l,words)
#判断一个单词是否符合要求
isvalide = lambda word,s:len(filter(lambda x:s.find(x)<0,word))==0
#寻找全部符合条件单词
filterwords = lambda words,c:filter(lambda x:isvalide(x,c),words)

#装载常用词汇
def loadwords(name):
    global words
    d=open(name).read()
    for line in d.split('\n'):
        if(len(line)==0):continue
        words.append(line.split()[0])
    words=list(set(words)) #去除重复词汇,重新排序
    words.sort()
#测试词汇
def testpro(name,s):
    t=open(name).read().split()
    t=list(set(t))
    l=maxwordlen(t)
    print '最长单词字母数:',l,'最长单词',maxword(t,l)
    a=filterwords(t,s)
    l=maxwordlen(a)
    print '测试条件:',s,'符合条件单词数目:',len(a)
    print '符合条件最长单词字母数:',l,'符合条件最长单词',maxword(a,l)
if __name__ == '__main__':
    loadwords('d:/longman.txt')
    print '总词库大小:',len(words)
    ans=filterwords(words,sp)
    print '测试条件:',sp,'\n符合条件单词数目:',len(ans)
    #print '\n'.join(ans)
    print '\n下面是机械专业词汇测试'
    testpro('d:/jx.txt',sp)
    print '\n下面是地质专业词汇测试'
    testpro('d:/d.txt',sp)
    print '\n下面是地质专业词汇测试'
    testpro('d:/d.txt','bcdefghijklmnopqrstuvwxyz')



