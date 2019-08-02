list = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]

def BubbleSort(list1):
    for i in range(0, len(list1) - 1):
        for j in range(0, len(list1) - i - 1):
            if(list1[j] > list1[j + 1]):
                temp = list1[j]
                list1[j] = list1[j + 1]
                list1[j + 1] = temp
    return list1

print(BubbleSort(list))