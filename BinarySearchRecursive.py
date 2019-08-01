sortedList = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def binSearch(list2, num, start, end):
    if (start > end):
        return False
    # avoid integer overflow that results if we use (start+end)/2
    mid = start + (end - start) // 2
    # if found
    if(list2[mid] == num):
        return True
    # if > then take initial half of list
    if(list2[mid] > num):
        return binSearch(list2, num, start, mid - 1)
    # if < then take later half of list
    if(list2[mid] < num):
        return binSearch(list2, num, mid + 1, end)

print(sortedList)
search = int(input("Enter number to search in list: "))

if (binSearch(sortedList, search, 0, len(sortedList) - 1)):
    print("Item Found!")
else:
    print("Item not in list!")
