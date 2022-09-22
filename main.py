import time

TTL = 3  # time to live for saving calculated values


# binary search a list of lists
# index is the index of the inner list item
def binary_search_list(list, index=0, key=0):
    # list is a list of tupels that contain tupel of keys and ttl
    curr_time = time.time()
    i = int(len(list) / 2)
    if not list:
        return -1
    while i > 0:
        if curr_time - list[i][index] < key:
            i = int(i + i / 2)
        elif curr_time - list[i][index] > key:
            i = int(i - i / 2)
        else:
            return i
        if curr_time - list[i][index] < key:
            return i
    if curr_time - list[0][index] < key:
        return 0
    return -1


# cleans all items in list starting from index i
def clean_expired_items(list, i, ttl, vals):
    while i >= 0:
        vals.pop(list[i][2])
        ttl.pop(list[i][2])
        list.pop(i)
        i -= 1

# resets the TTL of list[i] in all the relevant data structures (list, ttl_dict)
def reset_ttl(list, i, ttl_dict):
    temp = list.pop(i)
    curr_time = time.time()
    ttl_dict[temp[2]] = curr_time
    list.append((temp[0], curr_time, temp[2]))
    return list[-1][0]


#  decorator function that apllies cache with TTL on every function that it wraps

def decorator(original_func):
    funcs = {}
    ttl = {}  # value is argument key is time of calculation
    vals = {}  # value is argument key is return value of original function

    def wrapper_func(*args, **kwargs):
        if original_func.__name__ not in funcs:
            funcs[original_func.__name__] = []
        # clean expired items
        i = binary_search_list(funcs[original_func.__name__], index=1, key=TTL)
        if i != -1:
            # check if recent key is within ttl
            if (i + 1) == len(funcs[original_func.__name__]):
                val = reset_ttl(funcs[original_func.__name__], i, ttl)
                print(f"ttl of input {args} for {original_func.__name__}() was reset")
                return val
            clean_expired_items(funcs[original_func.__name__], i, ttl, vals)
        # calculate
        print(f"wrapper calculating {original_func.__name__} with args: {args}")
        val = original_func(*args, **kwargs)
        curr_time = time.time()
        funcs[original_func.__name__].append((val, curr_time, args))
        ttl[args] = curr_time
        vals[args] = val
        return val

    return wrapper_func


@decorator
def add(a, b):
    return a + b


@decorator
def square(num):
    return num * num


print(square(2))
print(square(3))
print(square(3))
print(square(3))
print(add(5,7))
print(square(2))
time.sleep(3.1)
print(square(2))

print(add(2, 3))
print(add(2, 3))
