from lunar import *
def isLucky(m,d):
	if m<10:
		if m==d%10:return 1
	else:
		if d<10:
			if int(m/10)==d:return 1
		else:
			if int(m/10)==d%10 and m%10==int(d/10):
				return 1
	return 0
for year in range(1900,2000):
	for m in range(1,12):
		for d in range(1,29):
			if isLucky(m,d):
				x,y,z=get_ludar_date(datetime(year,m,d))
				if y*z!=0 and isLucky(y,z) and y+1==m\
				and d%10-1==z%10 and d//10-1==z//10:
					print(year,"sun",m,d,"lunar",y,z)