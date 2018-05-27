#!/usr/bin/env python3
# coding: utf-8

'模拟orm框架的简单写法，不使用mateclass'
class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class Model(dict):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        self.mapping = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                self.mapping[k] = v
        self.table = self.__class__.__name__

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.mapping.items():
            fields.append(v.name)
            params.append('?')
            args.append(self[k])
        sql = 'insert into %s (%s) values (%s)' % (self.table, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))


class User(Model):

    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('user_name')
    email = StringField('email')
    password = StringField('password')


# 创建一个实例：
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
# 保存到数据库：
u.save()
print(u.__dict__)
