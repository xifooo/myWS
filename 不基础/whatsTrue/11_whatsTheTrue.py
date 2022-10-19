class A:
    ...
    
def f():
    ...
    
def whats_true(d:dict):
    for i in d.keys():
        if d[i] is True:
            print(f'\"{i}\" is True')
            
        if d[i] == True:
            print(f'\"{i}\" == True')
            
        if d[i]:
            print(f'\"{i}\" if True')
            
        if bool(d[i]):
            print(f'\"{i}\" bool True')
            
        print("---------")
            

if __name__ == "__main__":
    
    d = {
    "True": True,
    "False": False,
    "None": None,
    
    "1": 1,
    "0": 0,
    "1.1": 1.1,
    "-1": -1,

    "空字符串": "",
    "字符串": "字符串",

    "class A": A(),
    "func f": f(),
    "空列表": [],
    "空字典": {},
    "空集合": ()
}
    
    whats_true(d)
        
