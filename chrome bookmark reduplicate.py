# -*- coding:utf-8 -*-
'''
chrome 书签同步处理脚本
用法：1.将chrome 书签导出到文件,与本脚本放置在同一文件夹
      2.将代码中开头filename改成刚导出文件名字
      3.运行脚本
      4.将chrome书签全部删除，同步中心数据清除，导入刚才处理完的数据
      5.根据喜好适当做些调整，登陆同步中心重新同步
      6.have fun
winxos 2012-9-17
'''
import re,collections

#使用时将下一行中的filename替换成导出书签名字
filename="bookmarks_12-9-17.html"

r='<A HREF="([^"]+)'
loadfile = lambda name:open(name).read() #读入书签文件
get_duplicated = lambda context:filter(  #得到重复书签的列表
  lambda x: x[1] > 1,
  collections.Counter(re.findall(r,context)).items())
def savefile (name,context):
  f=open(name,'w')
  f.write(context)
  f.close()
def remove(s,d):
  for item in d:
    pos=s.find(item[0])
    #注意过滤干扰正则的特殊符号 ?(){}+
    s=s[:pos+1]+re.sub(r'(<DT><A.*'+re.sub('[?(){}+]','.',item[0])+'.*</A>)','',s[pos+1:]) 
  return s
if __name__ == '__main__':
  rawf=loadfile(filename)
  print 'loaded.\ntotal bookmarks:',len(re.findall(r,rawf))
  dup=get_duplicated(rawf)
  print 'duplicated.\n',dup
  print 'waiting...'
  s=remove(rawf,dup)
  print 'success.\ntotal bookmarks:',len(re.findall(r,s))
  name='new_'+filename
  savefile(name,s)
  print 'save file to: ',name
  print 'done! remember reload to chrome.'