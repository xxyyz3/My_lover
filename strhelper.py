def reverse_str(s)->str:
    return s[::-1]
    # return ' '.join(s[::-1])
def count_char(s,char):
    return s.count(char)

def upper_all(s):
    return s.upper()
if __name__ == '__main__':
    print(reverse_str("sqw"))