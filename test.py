import natsort
import os
PATH = "/home/nick/Projects/BatchConverter/Data/Cell NETLC0022 Ni-GDC SSC-GDC PrO inf Ni-GDC inf/Data/"
flistlist = []
for i in natsort.natsorted(os.listdir(PATH)):
    if 'Aging' in i:
        for files in os.listdir(PATH + '/' + i + '/Run01/'):
            if '.z' in files:
                flistlist.append(files)
print(len(flistlist))
flistlist = natsort.natsorted(flistlist)

print(flistlist[179])