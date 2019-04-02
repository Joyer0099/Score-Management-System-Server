# MarkSystem

## 数据库约定

University: (id, name, shortname)

用于存放大学信息

College: (id, name, shortname, university(FK))

用于存放学院信息

外键：university

Teacher: (id, tid, password, name, college(FK), is_manager, email, mobile)

用于存放教师信息

外键：college

Token: (id, token_text, teacher(FK), create_time)

用于存放验证细腻洵

外键：teacher

Major: (id, name, shortname, college(FK))

用于存放专业信息

外键：college

Student: (id, sid, name, year, major(FK))

用于存放学生信息

外键：major

Lesson: (id, name, college(FK))

用于存放课程组信息

外键：college

ClassInfo: (id, name, teacher(FK), semester, week, room, cid, lesson(FK))

用于存放课程组内具体课程信息

外键：teacher, lesson

Class: (id, student(FK), classInfo(FK))

用于存放学生与课程信息的映射

外键：student, classInfo

TitleGroup: (id, name, lesson(FK), weight)

用于存放分数大项

外键：lesson

期中、期末成绩类别放在此处

Title: (id, name, titleGroup(FK), weight, classInfo(FK))

用于存放分数小项

外键：titleGroup, classInfo

客观分、主观分类别放在此处

Point: (id, classInfo(FK), student(FK), title(FK), pointNumber, date, note)

用于存放分数小项每个学生对应的得分数

外键：title, classInfo， student

#### Point和Title表的classInfo外键是否冗余
