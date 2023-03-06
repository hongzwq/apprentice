def insert_sort(A):
    if len(A) == 1:
        return A
    else:
        x = A[-1]
        B = insert_sort(A[:-1])
        i = 0
        while i < len(B):
            if x < B[i]:
                break
            i += 1
        B.insert(i, x)
        return B


if __name__ == '__main__':
    import random

    A = []
    for i in range(10):
        r = random.randint(1, 10)
        A.append(r)
    print(A)
    print(insert_sort(A))
