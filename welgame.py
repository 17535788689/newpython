arr =  32
num = 64
for i in range(num):
    for j in range(num):
        print(arr, end=' ')
        arr += 1
        if arr == num:
            arr = 0
            print()
        else:
            arr += 1
            print()
        if arr > num:
            break
            print("权重过大")
        else:
            False
            print("权重过小")