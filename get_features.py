def get_features(code_a: str, code_b: str):
    lines_a = code_a.split('\n')
    lines_b = code_b.split('\n')

    f4 = (len(lines_a) + len(lines_b)) / 2

    cnt = 0
    for i in range(len(lines_a)):
        for j in range(len(lines_b)):
            if lines_a[i] == lines_b[j]:
                cnt += 1
    f1 = cnt / (len(lines_a) * len(lines_b))

    if len(lines_a) < 2 or len(lines_b) < 2:
        return f1, 0, 0, f4

    cnt = 0
    for i in range(len(lines_a) - 1):
        for j in range(len(lines_b) - 1):
            if lines_a[i] == lines_b[j] and lines_a[i + 1] == lines_b[j + 1]:
                cnt += 1
    f2 = cnt / ((len(lines_a) - 1) * (len(lines_b) - 1))

    if len(lines_a) < 3 or len(lines_b) < 3:
        return f1, f2, 0, f4

    cnt = 0
    for i in range(len(lines_a) - 2):
        for j in range(len(lines_b) - 2):
            if lines_a[i] == lines_b[j] and lines_a[i + 1] == lines_b[j + 1] \
                    and lines_a[i + 2] == lines_b[j + 2]:
                cnt += 1
    f3 = cnt / ((len(lines_a) - 2) * (len(lines_b) - 2))

    return f1, f2, f3, f4
