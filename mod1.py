def sum(a,b):
    return a+b

def safe_sum(a,b):
    if type(a) != type(b):
        print ("변수가 타입이 상이합니다!")
        return
    else:
        result = a + b
    return a + b