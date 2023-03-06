def quick_sort(A):
    if len(A) == 1 or len(A) == 0:
        return A
    else:
        left = []
        right = []
        k = A[-1]
        for a in A[:-1]:
            if a <= k:
                left.append(a)
            else:
                right.append(a)
        return quick_sort(left) + [k] + quick_sort(right)


if __name__ == '__main__':
    import random

    A = []
    for i in range(10):
        r = random.randint(1, 10)
        A.append(r)
    print(A)
    print(quick_sort(A))
