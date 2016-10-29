#得到指定（阳历）日期的星期数
#公式来自网络搜集，感谢大仙
#winxos 2011-3-13
#y=year, m=month, d=day
def weekday(y,m,d):
    if m<3:
        d+=y
        y-=1
    else:
        d+=y-2
    return (23*m//9+d+4+y//4-y//100+y//400)%7
def show(n):
    a=["sun","mon","tur","wen","thr","fri","sat"]
    print a[n]
show(weekday(2008,2,13))
