list1 = [1] * 4
list2 = [5, 5, 5]
while not False:
    list1[0] += 1
    if list1[0] == 5: 
         break
         list1[1] += 2
    list1[2] += 3

print(list1 < list2)
print(list2 == (5, 5, 5))
