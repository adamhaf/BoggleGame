# FILE : .py
# WRITER : Adam Haftzadi , adamhaf , 315359737
# EXERCISE : intro2cs2 ex 2021
# DESCRIPTION:

def last_in(x):
    def get():
        temp = last_in.__dict__.get('prev', None)
        last_in.__dict__['prev'] = x
        return temp
    return get()

print(last_in(1))
print(last_in(2))
print(last_in(1))