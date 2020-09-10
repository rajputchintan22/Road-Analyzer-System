fp1 = open("D:\Test\Show2\Final.txt")
l1 = fp1.readlines()
l1 = [x for x in l1 if x != '\n']
fp1.close()
fp2 = open("D:\Test\Show2\my_final.csv")
l2 = fp2.readlines()
print(len(l2))
l2[0] = l2[0].replace('\n', ','+"Lat,Long\n")
for i in range(1, len(l1)+1):
    l2[i] = l2[i].replace('\n', ','+l1[i-1])

l2 = l2[:len(l1)+1]
fp2 = open("D:\Test\Show2\my_final.csv", 'w')
fp2.writelines(l2)
fp2.close()