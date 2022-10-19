from base_01 import db,Student

# # # 增
# s1 = Student(s_name='张三', s_gender='男', s_phone='123123123')
# s2 = Student(s_name='wd', s_gender='男')
# s3 = Student(s_name='gdd', s_gender='男', s_phone='12313')
# # db.session.add(s1)
# s = [s1,s2,s3]
# db.session.add_all(s)
# db.session.commit()


# 删



# 查
# get(id)查询单个
stu = Student.query.get(100)
print(stu.s_name)

# all()查询全部
stu1 = Student.query.all()
for _ in stu1:
    print(_.s_name, _.s_gender, _.s_phone)
    
# filter() 条件查询
# stu2 = Student.query.filter(Student.s_id <= 3)
stu2 = Student.query.filter(Student.s_gender == '男')
for _ in stu2:
    print(_.s_name, _.s_gender, _.s_phone)
    
# filter_by() 类似sql的查询 first() 查询到的第一个
# stu3 = Student.query.filter_by(s_id <= 3)
# stu3 = Student.query.filter_by(Student.s_name == '张三').all()
stu3 = Student.query.filter_by(Student.s_name == '张三').filter(Student.s_id >= 2)
for _ in stu3:
    print(_.s_name, _.s_gender, _.s_phone)
    
    
    

# 改