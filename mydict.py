# coding: utf-8

class MyDict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = MyDict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = MyDict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kv):
        super().__init__(**kv)

    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, k, v):
       self[k] = v

if __name__ == '__main__':
    # 文档测试
    import doctest
    doctest.testmod()

    mydict = MyDict(name='francis', age=25)
    print(mydict['name'])
    print(mydict.age)


