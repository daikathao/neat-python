import random

X_train = []
y_train = []
for x in range(100):
    t1 = random.randint(1, 99)
    t2 = random.randint(1, 99)
    X_train.append((t1, t2))
    if (t1 + t2) % 3 == 0:
        y_train.append(1)
    else:
        y_train.append(0)



X_test = []
y_test = []
for x in range(10):
    t1 = random.randint(111, 333)
    t2 = random.randint(111, 222)
    X_test.append((t1, t2))
    if (t1 + t2) % 3 == 0:
        y_test.append(1)
    else:
        y_test.append(0)