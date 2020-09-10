fp = open('D:\\Test\\Show2\\my_final.csv', 'r')
l = fp.readlines()
fp.close()
for i in range(0, len(l)):
    l[i] = l[i].replace('\n','')
l.sort()
final = []
print(l)
for i in range(0, len(l), 3):
    temp = [0, '', '', '']
    if "good road" in l[i]:
        temp[2] = 'good road'
        l[i] = l[i].replace(',good road', '')
        l[i] = l[i].replace('_center_', '')
        temp[0] = int(l[i])
    else:
        temp[2] = 'bad road'
        l[i] = l[i].replace(',bad road', '')
        l[i] = l[i].replace('_center_', '')
        temp[0] = int(l[i])
    if "good road" in l[i+1]:
        temp[1] = 'good road'
    else:
        temp[1] = 'bad road'
    if "good road" in l[i+2]:
        temp[3] = 'good road'
    else:
        temp[3] = 'bad road'
    final.append(temp)
final.sort()
fp = open('D:\\Test\\Show2\\my_final.csv', 'w')
for i in final:
    temp = ",".join(i[1:])
    temp = str(i[0]) + "," + temp
    temp += '\n'
    fp.write(temp)
fp.close()
fp = open('D:\\Test\\Show2\\my_final.csv', 'r')
l = fp.readlines()
fp.close()
for i in range(0, len(l)):
    l[i] = l[i].replace('\n','')
final = []
print(l)
for i in l:
    temp = [0, 0, 0, 0, 0]
    temp2 = i.split(',')
    temp[0] = int(temp2[0])
    if temp2[1] == 'bad road':
        temp[1] = 1
        temp[4] = -2
    if temp2[2] == 'bad road':
        temp[2] = 1
        temp[4] = 1
    if temp2[3] == 'bad road':
        temp[3] = 1
        temp[4] = 2
    if temp[1] + temp[2] + temp[3] > 1:
        temp[4] = 1
    final.append(temp)
final.sort()
fp = open('D:\\Test\\Show2\\my_final.csv', 'w')
fp.write("Frame No.,Left,Center,Right,Type\n")
for i in final:
    temp = str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "," + str(i[4])
    temp += '\n'
    fp.write(temp)
fp.close()

