import datetime
# data=datetime.date.today()
# print(data)
# d=datetime.date(2024,12,8)
# print(d-data)
# nedela=datetime.timedelta(days=7)
# print(nedela+data)
# e=7
# s=1
# spisoc=[]
# while e>0:
#     dni=datetime.timedelta(days=s)
#     data=datetime.date.today()
#     r=dni+data
#     s=s+1
#     e=e-1
#     spisoc.append(str(r))
# print(spisoc)
d=datetime.time(7,30,30)
spisoc=[]
w=8
while w<18:
    chasi=datetime.time(w,0,0)
    spisoc.append(str(chasi))
    w=w+1
print(spisoc)
