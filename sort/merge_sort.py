def merge_sort(A):
    def merge(left, right):
        r, l = 0, 0
        result = []
        while l < len(left) and r < len(right):
            if left[l] <= right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        result += left[l:]
        result += right[r:]
        return result

    if len(A) == 1:
        return A
    else:
        index = len(A) // 2
        left = A[:index]
        right = A[index:]
        left = merge_sort(left)
        right = merge_sort(right)
        return merge(left, right)


if __name__ == '__main__':
    import random

    A = []
    for i in range(10):
        r = random.randint(1, 10)
        A.append(r)
    print(A)
    print(merge_sort(A))
