# API design
[TOC]
# API STD
+ GET （SELECT）：从服务器检索特定资源，或资源列表。
+ POST （CREATE）：在服务器上创建一个新的资源。
+ PUT （UPDATE）：更新服务器上的资源，提供整个资源。
+ PATCH （UPDATE）：更新服务器上的资源，仅提供更改的属性。
+ DELETE （DELETE）：从服务器删除资源。
# API follow STD
+ 所有 url 应当被**小写**
+ 禁止使用动词作为 url
+ 如果未加任何筛选条件(通常为参数，即未携带任何参数)，默认不返回任何项。
+ 用户主体为网页客户端和智能手机客户端。

# URL head
```
xxx.xxxxxxx.xx/api/v1/
```

# 版本号
1.0 实现网站所需基本功能

1.1 增加修改个人信息功能，以及部分数据分析端功能

# 服务器返回状态码
`英文状态码(正式运行时启用)`

```
2--- 表示成功

'2000': 'OK, with Response',
'2001': 'OK, Add new resrource',
'2002': 'OK, Request accepted',
'2004': 'OK, No Response content',
'2005': 'OK, And need to Refresh',


4--- 表示失败
-01- 表示用户 token 认证失败
'4010': 'Error, Require token',
'4011': 'Error, Bad token',
'4012': 'Error, Token out of date',
'4014': 'Error, Forbidden token',
'4018': 'Error, Too much connections',

-02- 表示用户身份认证失败
'4020': 'Error, User is not exist',
'4021': 'Error, Username or password is incurrent',
'4022': 'Error, User out of date',
'4024': 'Error, Forbidden user',
'4027': 'Error, No authorized permissions',

-03- 表示请求本身错误
'4030': 'Error, No match API',
'4031': 'Error, No match Request Type',
'4032': 'Error, Missing parameters',
'4033': 'Error, Not Allowed',
'4035': 'Error, Gone',
'40329': 'Error, Too Many Requests',


5--- 表示服务器失败
'5001': 'Server is outline',
'5003': 'Can not access database',
'5004': 'Gateway Forbidden',
'5101': 'Server is updating',
'5201': 'Service Stopped'
```

`中文状态码(调试时启用)`    

```  
2--- 表示成功

'2000': '成功，服务器已响应',
'2001': '成功，服务器添加新资源',
'2002': '成功，请求被接收',
'2004': '成功，无响应内容',
'2005': '成功，资源需要被刷新',


4--- 表示失败
-01- 表示用户 token 认证失败
'4010': '错误，需要token验证',
'4011': '错误，无效的token',
'4012': '错误，过期的token',
'4014': '错误，被禁止的token',
'4018': '错误，连接次数过多',

-02- 表示用户身份认证失败
'4020': '错误，用户不存在',
'4021': '错误，用户名或密码错误',
'4022': '错误，用户登录已过期',
'4024': '错误，用户被禁止访问',
'4027': '错误，权限认证不通过',

-03- 表示请求本身错误
'4030': '错误，没有符合的API',
'4031': '错误，没有符合的请求类型',
'4032': '错误，参数缺失',
'4033': '错误，请求被拒绝',
'4035': '错误，已走远',
'40329': '错误，请求次数过多',


5--- 表示服务器失败
'5001': '服务器已离线',
'5003': '无法连接数据库',
'5004': '网管禁止',
'5101': '服务器更新中',
'5201': '服务已停止'
```


# Tree View
```bash
v1
|- /table
|     |- /lesson
|           |- /format
|      
|     |- /class_field
|           |- /wrapper
|           |- /format
|      
|     |- /class_info
|           |- /detail
|                 |- /all
|                 |- /some
|           |- /format
|
|- /user
|     |- /info  
|           |- /display
|           |- /format
|           |- /manage
|      
|     |- /login
|     |- /logout
|     |- /logon
|
|- /student
|     |- /display
|     |- /format
|
|- /university
|     |- /format
|
|- /college
|     |- /display
|     |- /format
|
|- /major
|     |- /format
|
|- /point
|     |- /display
|     |- /format
|     |- /import_data
|
|- /title
|     |- /display
|     |- /format
|
|- /titleGroup
|     |- /format
|
|- /analysis
|     |- /student
|           |- /name
|     |- /score
|           /- format
|           /- all
|

```
# API Lists  

`display只支持GET方法，请求方式与format一致`

---

## `/table/lesson`(todo)

---

## `/table/lesson/format`
`GET` `POST` `PUT` `DELETE`
教学班所属的课程组

### `GET` 查询课程组 (如「英语听说课」)
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Params     

| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | optional |
| **name** | string | optional |
| **college_id** | integer | optional |
| **all** | boolean | optional, 是否返回所有的课程组, 会忽略(id,name和college_id)筛选项 |

###### Response

```json
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 1,
            "name": "英语学术听说",
            "college_id": 1
        },
        {
            "id": 2,
            "name": "英语电影视听说",
            "college_id": 1
        }
    ],
    "count": 2,
    "all": "1"
}
```

### `PUT` 更改课程组
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |
| **name**    | string | optional |
| **college_id** | integer | optional |
+ 示例  

```json
{
  "subjects":[
    {
      "id":1,
      "name":"不实用英语会话",
      "college_id":1
    }
    ...
  ]
}
```

###### Response
成功返回  

```
{
    "subjects": [
        {
            "id": 1
        }
    ],
    "code": "2005",
    "message": "OK, And need to Refresh"
}  

```
无任何更改返回
```
2004 
```
其它失败时返回
```
4032
```

### `POST` 添加新课程组
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Body

| params | 类型 | 说明 |
| --- | --- | --- |
| **name**    | string | required |
| **college_id** | integer | required |
+ 示例  

```json
{
	"subjects":[
		{
			"id":1,
			"name":"英语学术视听说",
			"college_id":1
		}	
		
	]
	
	
}
```

###### Response
成功返回  

```  
{  
    "subjects": [  
        {  
            "id": 3  
        }  
    ],  
    "code": "2001",
    "message": "OK, Add new resrource"
}  

```
失败时返回
```
2004
```

### `DELETE` 删除课程组
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Body
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required
+ 示例  

```json
{
  "subjects":[
    {
      "id":1,
    }
    ...
  ]
}
```

###### Response
成功返回  

```
{
    "code": "2005",
    "message": "OK, And need to Refresh"
}  
```
没有成功删除则返回
```
2004  
```
其它失败时返回
```
4032  
```

---

## `/table/class_field/` (todo)

---

## `/table/class_field/wrapper`
`GET`

返回教学班组织信息(即教学班和学生的多对多关系)

### `GET` 根据筛选选项获取教学班拥有学生数及学生的id

###### Head

需要 `X-Access-Token`，携带内容为用户 token

###### Params

| params | 类型 | 说明 |
|---|---|---|
| **id**      | integer | optional，以教学班的数据库主键编号为筛选项
| **classInfo_id**    | integer | optional，以课程所属的课程组为筛选项
| **student_id**    | integer | optional，以学生的数据库主键编号为筛选项查找(该学生参加的)课程

###### Response
```json
200 OK

JSON
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 293,
            "student_id": 315,
            "classInfo_id": 39
        }
    ],
    "count": 1
}
```
具体的返回值包含所有满足筛选项的查询结果在 Class 表中的内容，具体字段参见数据库相关文档。

若查询失败返回 `400 Bad Request`，若查询结果为空，返回`204 No Content`

## `/table/class_field/format`
`GET` `POST` `DELETE`
教学班和学生的关系不应该被修改，如果注册了错误的学生，应该将其删除并另行添加。

### `GET` 根据筛选项获取教学班组织信息(即教学班与学生的多对多关系)
再次强调，在无筛选项时不会返回任何班级的信息。

+ 对学生信息的修改会触发本接口对应的表额外的修改。  

###### Head  

需要 `X-Access-Token`，携带内容为用户 token  

###### Params  

获取教学班组织信息(即教学班和学生的多对多关系)。若筛选项为空，不返回任何课程。  

| params | 类型 | 说明 |
|---|---|---|
| **id**      | integer | optional，以教学班的数据库主键编号为筛选项
| **classInfo_id**    | integer | optional，以课程所属的课程组为筛选项
| **student_id**    | integer | optional，以学生的数据库主键编号为筛选项查找(该学生参加的)课程

###### Response
```json
200 OK

JSON
{
  ...
  "subjects":[
    {
      "id":112,
      "lesson":1,
      "student":1334124,
      "sid":"2018211511",
      "sname": "赵茶茶",
      "index": "01",
    },
    {
      "id":113,
      "lesson":1,
      "student":1334125,
      "sid":"2018211512",
      "sname": "钱叶叶",
      "index": "02",
    },
    {
      "id":114,
      "lesson":1,
      "student":1334126,
      "sid":"2018211513",
      "sname": "孙树树",
      "index": "03",
    },
    ...
  ],
  "count":32
}
```
具体的返回值包含所有满足筛选项的查询结果在 Class 表中的内容，具体字段参见数据库相关文档。

若查询失败返回 `400 Bad Request`，若查询结果为空，返回`204 No Content`

### `POST` 添加新的返回教学班组织信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token

###### Body
提交时对象必须包含「必须」的字段。

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required, 教学班在数据库中的主键编号 |
| **classInfo_id**    | integer | required, 教学班id |
| **student_id**    | integer | required, 学生id |
| **index**    | string | optional, 学生在教学班班内编号 |

+ 示例  

```json

JSON
{
  "subjects": [
    {
      "classInfo_id":1,
      "student_id":1,
    }

  ]
 ...
}
```

###### Response
若成功添加资源，返回
```
205 Reset Content
```
若失败，返回
```
400 Bad Request
```

### `DELETE` 删除教学班组织信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Body
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required

+ 示例  

```json
{
  "subjects":[
    {
      "id":1,
    }
    ...
  ]
}
```
###### Response
成功返回  

```
{
    "code": "2005",
    "message": "OK, And need to Refresh"
}  
```
没有成功删除则返回
```
2004  
```
其它失败时返回
```
4032  
```

---

## `/table/class_info`(todo)

---

## `/table/class_info/detail/all`
`GET`

管理员获取到所有课程信息

###### Head
需要 `X-Access-Token`，携带内容为用户 token，用于验证身份信息以及寻找到当前教师及其对应角色

###### Response
```json
200 OK

JSON
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 1,
            "name": "英语学术听说1班",
            "semester": "2018秋季",
            "week": "4-18单周",
            "room": "3-319",
            "cid": "001",
            "teacher_id": 1,
            "teacher_message": {
                "id": 1,
                "tid": "20182018",
                "password": "password1",
                "name": "Mr zero",
                "college": 1,
                "is_manager": true,
                "email": "",
                "mobile": ""
            },
        }
        ......
    ],
    "count": 26
}
```

若查询失败返回 `400 Bad Request`，若查询结果为空，返回`204 No Content`


## `/table/class_info/detail/some`
`GET`

任课教师获取到个人课程信息

###### Head
需要 `X-Access-Token`，携带内容为用户 token

###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional，以 class(教学班)的数据库主键为筛选项筛选课程 |
| **name**      | string  | optional，以 name 为搜索项进行模糊匹配 |
| **cid**       | string | optional，以课程代号为筛选项筛选课程 |
| **lesson_id** | integer | optional，以课程id为搜索项进行匹配 |
| **teacher_id**   | integer | optional，以教师(或管理员)数据库主键为查询条件查询教师所执教的所有课程 |
| **semester**      | string  | optional，以 semester 为搜索项进行模糊匹配 |
| **week**     | string | optional，以 week 为搜索项进行模糊匹配 |
| **room**      | string | optional，以 room 为搜索项进行模糊匹配 |

###### Response
```json
200 OK

JSON
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 2,
            "name": "英语学术听说1班",
            "semester": "2018秋季",
            "week": "4-18单周",
            "room": "3-319",
            "cid": "002",
            "teacher_id": 1,
            "teacher_message": {
                "id": 1,
                "tid": "20182018",
                "name": "Mr Joe",
                "college": 1,
                "is_manager": false,
                "email": "",
                "mobile": ""
            },
        }
        ......
    ],
    "count": 3
}
```

若查询失败返回 `400 Bad Request`，若查询结果为空，返回`204 No Content`

## `/table/class_info/format`
`GET` `PUT` `POST` `DELETE`

教学班的辅助信息。

### `GET` 获取课程的全部辅助信息
###### Head
需要 `X-Access-Token`，携带内容为用户 token
###### Params
获取课程的具体信息，包括 core 部分和 support 部分。若筛选项为空，不返回任何课程。 

 

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional，以 class(教学班)的数据库主键为筛选项筛选课程 |
| **name**      | string  | optional，以 name 为搜索项进行模糊匹配 |
| **cid**       | string | optional，以课程代号为筛选项筛选课程 |
| **teacher_id**   | integer | optional，以教师(或管理员)数据库主键为查询条件查询教师所执教的所有课程 |
| **semester**      | string  | optional，以 semester 为搜索项进行模糊匹配 |
| **week**     | string | optional，以 week 为搜索项进行模糊匹配 |
| **room**      | string | optional，以 room 为搜索项进行模糊匹配 |
| **lesson_id** | integer | optional，以课程id为搜索项进行匹配 |

###### Response
```json
200 OK

JSON
{
  "subjects": [
    {
      "id":1,
      "name":"英语口语听说311班",
      "teacher":12314,
      "year": "2014",
      "month": "09",
      "date": "Friday,11-18 week ",
      "room": "base 3 502",
    }
  ]
  ...
}
```
若查询失败返回 `400 Bad Request`，若查询结果为空，返回`204 No Content`
### `POST` 添加新的返回教学班辅助信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token

###### Body
提交时对象必须包含「必须」的字段。

| params | 类型 | 说明 |
|---|---|---|
| **name**      | string  | required |
| **teacher_id**   | integer | required |
| **lesson_id** | integer | required |
| **semester**      | string  | optional |
| **week**     | string | optional |
| **room**      | string | optional |
| **cid** | string | optional |

+ 示例  


```json

JSON
{
  "subjects": [
    {
      "classInfo_id":1,
      "student_id":1,
    }

  ]
 ...
}
```

###### Response
若成功添加资源，返回
```
205 Reset Content
```
若失败，返回
```
400 Bad Request
```
### `PUT` 更改课程辅助信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
所添加的课程的授课教师不一定必须为提交 post 的用户。

###### Params

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | required |
| **name**      | string  | optional |
| **teacher_id**   | integer | optional |
| **semester**      | string  | optional |
| **week**     | string | optional |
| **room**      | string | optional |
| **lesson_id** | integer | optional |

+ 示例  

```json
PUT
{
"subjects": [
  {
    "id":1,
    "name":"英语口语听说311班",
    "teacher":12315,
    "date": "Friday,11-18 week",
    "room": "base 3 504",
  },
  {
    "id":2,
    "name":"英语口语听说312班",
    "teacher":12315,
    "room": "base 3 504",
    "_i_m_comment_": "比如修改了教师和教室"
  }]
}
```



###### Response
成功创建时返回创建/修改的课程信息的 id  

```json
201 Created / 205 Reset Content

json
{
  "subjects":[
    {
      "id":[1,2]
    }
  ],
  "id":[1,2]
}
```

若创建失败，或若请求非法，未通过校验，返回 400
```
400 Bad Request
```


### `DELETE` 删除已有的课程信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token

###### Body
提交时对象必须包含正确的 id 字段。
其余选项不会被读入，没有必要包含。

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |

+ 示例  

```json

json
{
"total": 1,
"subjects": [
    {
        "id": 15,
        "_this_is_another_comment":"下面这些都可以不要",
        "room": "教3 504",
        "name":"英语口语听说311班",
        "teacher":12314,
        "year": "2014",
        "month": "09",
        "date": "Friday,11-18 week ",
        "room": "base 3 502",
    }
],
...
}
```


###### Response
若成功删除资源，返回
```
205 Reset Content
```
若失败，返回
```
400 Bad Request
```

---

## `/user`(todo)

---

## `/user/info`(todo)

---

## `/user/info/display`
`GET`

### `GET` 获取用户所有信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Params
字段类型与数据库字段相同，注意 is_manager 字段返回值为 0,1。  

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional |
| **tid**        | string | optional |
| **name**      | string | optional |
| **college_id**   | integer | optional |
| **email**     | string | optional |
| **mobile**    | string | optional |
| **is_manager**   | boolean | optional |

###### Response
返回时将不会返回 password (密码)字段

```json
200 OK

{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 1,
            "tid": "20182018",
            "name": "Mr zero",
            "is_manager": true,
            "email": "",
            "mobile": "",
            "college_id": 1,
            "college_message": {
                "id": 1,
                "name": "语言与传播学院",
                "shortname": "yycb",
                "university_id": 1
            },
            "university_message": {
                "id": 1,
                "name": "北京交通大学",
                "shortname": "BJTU"
            }
        }
    ],
    "count": 1
}
```

请求失败时返回 `400 Bad Request`

查询失败时返回`204 No Content`

## `/user/info/format`
`GET`

### `GET` 获取用户的信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Params
字段类型与数据库字段相同，注意 is_manager 字段返回值为 0,1。  

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional |
| **tid**        | string | optional |
| **name**      | string | optional |
| **college_id**   | integer | optional |
| **email**     | string | optional |
| **mobile**    | string | optional |
| **is_manager**   | boolean | optional |

###### Response
返回时将不会返回 password (密码)字段  

```json
200 OK

json
{
  "subjects":[
    {
      "id": 14424,
      "tid": "314123",
      "name": "冯天佑",
      "collage": 502,
      "manager": false,
      "email": "",
      "mobile": null,
    }
  ]
}  

```
请求失败时返回
```
400 Bad Request
```
查询失败时返回
```
204 No Content
```

### `PUT` 更改当前登录用户信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token

###### Body
| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | required |
| **name** | string | optional |
| **college_id** | integer | optional |
| **email** | string | optional |
| **mobile** | string | optional |
| **old_password** | string | required |
| **new_password** | string | optional |

+ 示例

```json
PUT
{
  "subjects": [
    {
      "id": 8,
      "name": "张云龙",
      "college_id": 2,
      "email": "1313240583@qq.com",
      "mobile": "13813801380",
      "old_password": "123456"
      "new_password": "654321"
    }
  ]
}

```

###### Resonpse

成功时返回

```
{
    "code": "2005",
    "message": "OK, And need to Refresh"
}  
```

更新失败则返回
```
{
    "code": "4038",
    "message": "Error, Data Update Failed"
}  
```

密码验证失败则返回
```
{
	'code': 4021, 
	'message': "Error, Username or password is incorrect"
}
```

## `/user/info/manage`
`GET` `PUT` `POST` `DELETE`
用户的全部信息。需要管理员权限。
***仅在该url下才可以进行用户的添加/修改/删除


### `GET` 获取用户的信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Params
字段类型与数据库字段相同，注意 manager 字段返回值为 0,1。  

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional |
| **tid**        | string | optional |
| **name**      | string | optional |
| **college_id**   | integer | optional |
| **email**     | string | optional |
| **mobile**    | string | optional |
| **is_manager**   | boolean | optional |

###### Response
返回时将会包括 password (密码)字段  

```json
200 OK

json
{
  "subjects":[
    {
      "id": 14424,
      "tid": "314123",
      "name": "冯天佑",
      "collage": 502,
      "password": "123456",
      "manager": false,
      "email": "",
      "mobile": null,
    }
  ]
}  

```
请求失败时返回
```
400 Bad Request
```
查询失败时返回
```
204 No Content
```

### `POST` 创建新用户
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body
| params | 类型 | 说明 |
|---|---|---|
| **tid**        | string | required |
| **name**      | string | required |
| **password** | string | required |
| **college_id**   | integer | required |
| **email**     | string | optional |
| **mobile**    | string | optional |
| **is_manager**   | boolean | optional, 默认为否 |

+ 示例  

```json
json
{
  "subjects":[
    {
      "tid": "314123",
      "name": "冯天佑",
      "collage": 502,
      "password": "123456",
      "manager": false,
      "email": "",
      "mobile": null,
      "password":123456
    }
  ]
}
```

###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

查询失败时返回
```
204 No Content
No match student(s)
```

### `PUT` 更改用户信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **tid**        | string | optional |
| **name**      | string | optional |
| **password** | string | optional |
| **college_id**   | integer | optional |
| **email**     | string | optional |
| **mobile**    | string | optional |
| **is_manager**   | boolean | optional, 默认为否 |

+ 示例  

```json
json
{
  "subjects":[
    {
    	"id": "1",
      "tid": "314123",
      "name": "冯天佑",
      "collage": 502,
      "password": "123456",
      "manager": false,
      "email": "",
      "mobile": null,
      "password":123456
    }
  ]
}
```
###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

查询失败时返回
```
204 No Content
No match student(s)
```
### `DELETE` 删除指定的用户
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required 筛选指定 id 的用户/学生 |

###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

查询失败时返回
```
204 No Content
No match student(s)
```

---

## `/user/login`
`POST`
### `POST` 用户登陆
###### Body

| params | 类型 | 说明 |
|---|---|---|
| **tid**        | string | required |
| **password** | string | required |
+ 示例  

```
{
	"tid": "admin",
	"password": "admin"
}
```



###### Response
回应内容为 token，是一串包含注明了用户 id (即token拥有者)的字符串
```
200 OK
{
    "token": "userid:2313 sasdasdzxasx"
}
```
失败时返回
```
400 Bad Request
```

---

## `/user/logout`
`POST`
### `POST` 登出用户
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Body
```
{}
```
`注销时无需在请求体中包含任何参数`
###### Response
```
205 Reset Content
```

---

## `/user/logon`
`POST`
### `POST` 注册用户
###### Body
| params | 类型 | 说明 |
|---|---|---|
| **tid**        | string | required |
| **name**      | string | required |
| **password** | string | required |
| **college_id**   | integer | required |
| **email**     | string | optional |
| **mobile**    | string | optional |
| **is_manager**   | boolean | optional, 默认为否 |

+ 示例  

```json
json
{
  "subjects":[
    {
      "tid": "314123",
      "name": "冯天佑",
      "collage": 502,
      "password": "123456",
      "manager": false,
      "email": "",
      "mobile": null,
      "password":123456
    }
  ]
}
```

###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

---

## `/student/`(todo)

---
## `/student/display`
`GET`

### `GET` 获取学生的完整信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Params


| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 筛选指定 id 的学生 |
| **sid**       | string | optional 筛选指定学号的学生 |
| **name**      | string | optional 筛选指定姓名的学生 |
| **major_id**     | integer | optional 筛选指定专业的学生 |
| **year**      | string | optional 筛选指定学年的学生 |
| **classInfo_id** | integer | optional 筛选指定教学班的学生 |

以classInfo_id 进行查询，返回该课程下的所有学生，忽略其他参数


###### Response
```json
200 OK

json
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 350,
            "sid": "17127471",
            "name": "应德辉",
            "year": "2019",
            "major_id": 1,
            "major_message": {
                "id": 1,
                "name": "英语",
                "shortname": "",
                "college_id": 1
            },
            "college_message": {
                "id": 1,
                "name": "语言与传播学院",
                "shortname": "yycb",
                "university_id": 1
            }
        }
    ],
    "count": 1
}
```
请求失败时返回
```
400 Bad Request
```
查询失败时返回
```
204 No Content
```


## `/student/format`
`GET` `PUT` `POST` `DELETE`
### `GET` 获取学生的基本信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token
###### Params


| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 筛选指定 id 的学生 |
| **sid**       | string | optional 筛选指定学号的学生 |
| **name**      | string | optional 筛选指定姓名的学生 |
| **major_id**     | integer | optional 筛选指定专业的学生 |
| **year**      | string | optional 筛选指定学年的学生 |
| **classInfo_id** | integer | optional 筛选指定教学班的学生 |

以classInfo_id 进行查询，返回该课程下的所有学生，忽略其他参数


###### Response
```json
200 OK

json
{
  "subjects":[
    {
      "id": 131,
      "sid": "2018141202",
      "name": "敦迟乌",
      "name": "2018",
      "major": 155,
    }
  ]
}
```
请求失败时返回
```
400 Bad Request
```
查询失败时返回
```
204 No Content
```

### `PUT` 更改学生的基本信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params  
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required 筛选指定 id 的用户/学生 |
| **sid**       | string | optional |
| **name**      | string | optional |
| **major_id**  | integer | optional |
| **year**      | string | optional |

###### Body
此处的 id 应与 Params 中的相吻合。

未包含的字段将不会进行更改。

```json
json
{
  "subjects":[
    {
      "id": 4,
      "name": "萨大成",
      "sid": "2014123113",
      "major": 155,
      "year": null,
    }
  ]
}
```

###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

查询失败时返回
```
204 No Content
No match student(s)
```

### `POST` 创建新用户/学生
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body
注意：若请求中包含 id 将会被忽略。

| params | 类型 | 说明 |
|---|---|---|
| **sid**       | string | required |
| **name**      | string | required |
| **major_id**  | integer | required |
| **year**      | string | optional |

+ 示例  

```json
json
{
  "subjects":[
    {
      "id": 14,
      "name": "冯天佑",
      "password": "12345678",
      "collage": 1,
      "year": null,
      "class_field": "502",
      "group": 1,
      "status": null,
      "manager": 0,
      "postion": "班长",
      "avatar": "https://avatar.hahaha.com",
      "email": "ju@hmail.com"
    }
  ]
}
```
###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

查询失败时返回
```
204 No Content
No match student(s)
```

### `DELETE` 删除指定的用户/学生
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
必须用 id 指定试图删除的学生。若包含其余的参数将会被忽略。  

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required 筛选指定 id 的用户/学生 |

###### Response
成功时返回
```
200 OK
```

请求失败时返回
```
400 Bad Request
```

查询失败时返回
```
204 No Content
No match student(s)
```

---

## `/university`(todo)

---

## `/university/format`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取大学相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 筛选指定 id 的大学 |
| **name**        | string | optional 通过名称筛选 |
| **shortname** | string | optional 通过昵称筛选 |

###### Response
```json
200 OK

{
	"subjects":[
        {
            "id": 2,
            "name": "University of Chinese Academy of Sciences",
            "shortname": "UCAS"
        }
	],
	"count":1,
	"total":1,
	"title":"university"
}
```


### `PUT` 更新大学相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**       | integer | required |
| **name**      | string | optional |
| **shortname**  | string | optional |

+ 示例  

```json
{
	"subjects":[
        {
            "id": 2,
            "name": "University of Chinese Academy of Sciences",
            "shortname": "UCAS"
        }
	]
}
```


###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `POST` 创建新的大学信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **name**      | string | required |
| **shortname**  | string | optional |

+ 示例  

```json
{
	"subjects":[
        {
            "id": 2,
            "name": "University of Chinese Academy of Sciences",
            "shortname": "UCAS"
        }
	]
}
```


###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `DELETE` 删除已有的大学信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body
| params | 类型 | 说明 |
|---|---|---|
| **id**       | integer | required |

+ 示例  

```json
{
  subjects:[{"id":2}，{"id":3}]
}
```


###### Response
```
205 Reset Content
```

---

## `/college`(todo)

---

## `/college/display`
`GET`
### `GET` 获取院系全部相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 筛选指定的院系 |
| **name**        | string | optional 通过名称进行字符串模糊匹配，会同时查询 `name` 和 `shortname` 字段 |
| **university_id** | integer | optional 查询大学所有的院系 

###### Response
```json
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 1,
            "name": "语言与传播学院",
            "shortname": "yycb",
            "university_id": 1,
            "university_message": {
                "id": 1,
                "name": "北京交通大学",
                "shortname": "BJTU"
            }
        }
    ],
    "count": 1
}
```


## `/college/format`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取院系相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 筛选指定的院系 |
| **name**        | string | optional 通过名称进行字符串模糊匹配，会同时查询 `name` 和 `shortname` 字段 |
| **university_id** | integer | optional 查询大学所有的院系 

###### Response
```json
{
  "subjects": [
      {
          "id": "1",
          "name": "Software Engine",
          "shortname": "SE",
          "university": "1"
      },
      {
          "id": "3",
          "name": "Art",
          "shortname": "Art",
          "university": "2"
      }
  ]
}
```

### `PUT` 更新院系相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | required |
| **name**      | string | optional |
| **shortname**  | string | optional |
| **university_id** | integer | optional |

+ 示例  

```json
{
    "subjects": [
        {
            "id": "1",
            "name": "Software Engine",
            "shortname": "SE",
            "university": "1"
        },
    ]
}
```
###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `POST` 创建新的院系信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body


| params | 类型 | 说明 |
|---|---|---|
| **name**      | string | required |
| **shortname**  | string | optional |
| **university_id** | integer | required |

+ 示例  

```json
{
    "subjects": [
        {
            "id": "1",
            "name": "Software Engine",
            "shortname": "SE",
            "university": "1"
        },
    ]
}
```
###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `DELETE` 删除已有的院系信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**      | integer | required |

+ 示例  

```json
{
  subjects:[{"id":2}，{"id":3}]
}
```


###### Response
```
205 Reset Content
```



---





## `/major`(todo)
---

## `/major/format`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取专业相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 筛选指定的专业
| **name**        | string | optional 通过名称进行字符串模糊匹配，会同时查询 `name` 和 `shortname` 字段
| **college_id** | integer | optional 查询院系所有的专业
###### Response
```json
{
  "subjects": [
      {
          "id": "1",
          "name": "Software Engine",
          "shortname": "SE",
          "college": 1,
      },
      {
          "id": "3",
          "name": "Modern Art",
          "shortname": "MA",
          "college": 155,
      }
  ]
}
```

### `PUT` 更新专业相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |
| **name**        | string | optional |
| **shortname**  | string | optional |
| **college_id** | integer | optional |

+ 示例  

```json
{
    "subjects": [
        {
            "id": "1",
            "name": "Software Engine",
            "shortname": "SE",
            "college": "1"
        },
    ]
}
```

###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `POST` 创建新的专业信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **name**        | string | required |
| **shortname**  | string | optional |
| **college_id** | integer | required |

+ 示例 

```json
{
    "subjects": [
        {
            "id": "1",
            "name": "Software Engine",
            "shortname": "SE",
            "college": "1"
        },
    ]
}
```

###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `DELETE` 删除已有的专业信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |

+ 示例

```json
{
  subjects:[{"id":2}，{"id":3}]
}
```

###### Response
```
205 Reset Content
```



---

## `/point`

---

## `/point/display`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取所有符合条件分数信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | optional，对id进行查询
| **classInfo_id** |integer| required，任何分数查询仅限于一科目内
| **student_id** |integer| optional，以加分对象(学生)进行查询
| **title_id** |integer| optional，以列名进行查询
| **date** |datetime| optional，以时间戳进行筛选
| **note** |string| optional，以备注进行字符串模糊匹配

返回 student_id 为 350 的学生所有成绩信息
```
@/point?leeson=2&type=0
```

###### Response
```
200 OK
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 579,
            "pointNumber": 52,
            "note": "",
            "student_id": 350,
            "title_id": 116,
            "classInfo_id": 39,
            "student_message": {
                "id": 350,
                "sid": "17127471",
                "name": "应德辉",
                "year": "2019",
                "major": 1
            },
            "title_message": {
                "id": 116,
                "name": "客观分",
                "titleGroup": 23,
                "weight": 100,
                "classInfo": 39
            },
            "classInfo_message": {
                "id": 39,
                "name": "MBA5班",
                "teacher": 30,
                "semester": "2019年秋季",
                "week": "1-19周",
                "room": "2教学楼",
                "cid": "",
                "lesson": 22
            }
        },
        ......
    ],
    "count": 2
}
```

## `/point/format`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取分数条目
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | optional，对id进行查询
| **classInfo_id** |integer| required，任何分数查询仅限于一科目内
| **student_id** |integer| optional，以加分对象(学生)进行查询
| **title_id** |integer| optional，以列名进行查询
| **date** |datetime| optional，以时间戳进行筛选
| **note** |string| optional，以备注进行字符串模糊匹配

返回 id 为 2 的课程所有加分类型为 0.出席 的加分项
```
@/point?leeson=2&type=0
```

###### Response
```
200 OK
{
  "subjects": [
      {
          "id": "1",
          "class": 201503,
          "student":10,
          "point": 3221,
          "title": 121,
          "date": ...,
          "note":null,
      },
      {
          "id": "2",
          "class": 201421,
          "student": 81,
          "point": 3144,
          "title": 1,
          "date": ..,
          "notes":...,
      }
  ],
  "title":"point"
}
```

### `PUT` 更新分数条目
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Params


###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | required |
| **classInfo_id** |integer| optional |
| **student_id** |integer| optional |
| **title_id** |integer| optional |
| **pointNumber** |integer| optional |
| **date** |datetime| optional |
| **note** |string | optional |

+ 示例  

``` json
{
  "subjects": [
      {
          "id": "1",
          "lesson": "2014211503",
          "student": "8102212004",
          "point": 32,
          "title": "Test 1"
      },
      {
          "id": "2",
          "lesson": "2014211503",
          "student": "8102212001",
          "point": 31,
          "title": "Test 1"
      }
  ],
  "title":"point"
}
```

###### Response
```
205 Rest Content
```
### `POST` 创建新的分数条目
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **classInfo_id** |integer| required |
| **student_id** |integer| required |
| **title_id** |string| required |
| **pointNumber** |integer| required |
| **date** |date| optional |
| **note** |varchar| optional |

+ 示例

``` json
{
  "subjects": [
      {
          "id": "1",
          "lesson": "2014211503",
          "student": "8102212004",
          "point": 32,
          "title": "Test 1"
      },
      {
          "id": "2",
          "lesson": "2014211503",
          "student": "8102212001",
          "point": 31,
          "title": "Test 1"
      }
  ],
  "title":"point"
}
```
###### Response 
```
205 Rest Content
```

### `DELETE` 删除已有的分数条目
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Params

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id** | integer | required

+ 示例

``` json
{
  "subjects": [
      {
          "id": "1",
          "lesson": "2014211503"
      },
      {
          "id": "2"
      }
  ],
  "title":"point"
}
```


###### Response
```
205 Rest Content
```

## `/point/import_data`
`POST`
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **title_list**        | dict list | required |
| **point_list** | dict list | required |
| **lesson_id** | integer | required |
| **sid_list** | integer list | required |

+ 示例

```json
{
    
}
```
###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

---

## `/title`

---

## `/title/display`
`GET`
### `GET` 获取小项相关所有信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 列id |
| **name**        | string | optional 列名 |
| **type** | integer | optional 小列的类别 (所在大列) |
| **titleGroup_id** | integer | optional 大列id |
| **classInfo_id** | integer | optional 教学班id|
###### Response
```json
{
    "code": "2000",
    "message": "OK, with Response",
    "subjects": [
        {
            "id": 101,
            "name": "主观分",
            "weight": 1,
            "titleGroup_id": 9,
            "classInfo_id": 17,
            "titleGroup_message": {
                "id": 9,
                "name": "化妆",
                "lesson": 18,
                "weight": 20
            },
            "classInfo_message": {
                "id": 17,
                "name": "戏班牙语",
                "teacher": 24,
                "semester": "2018年春季",
                "week": "123",
                "room": "4444444",
                "cid": "",
                "lesson": 18
            }
        },
        ...
    ],
    "count": 6
}
```

## `/title/format`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取小项相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 列id |
| **name**        | string | optional 列名 |
| **type** | integer | optional 小列的类别 (所在大列) |
| **titleGroup_id** | integer | optional 大列id |
| **classInfo_id** | integer | optional 教学班id|
###### Response
```json
{
  "subjects": [
      {
          "id": 12412412,
          "name": "Writing",
          "type": 1241,
          "weight": 1341(means 13.41),
      }
  ]
}
```

### `PUT` 更新小项相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |
| **name**        | string | optional |
| **weight** | integer | optional |
| **titleGroup_id** | integer | optional |
| **classInfo_id** | integer | optional |

+ 示例


```json
{
    "subjects": [
        {
          "id": 12412412,
          "name": "Writing",
          "type": 1241,
          "weight": 1341,
        },
    ]
}
```
###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `POST` 创建新的小项信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **name**        | varchar | required |
| **weight** | integer | optional |
| **titleGroup_id** | integer | required |
| **classInfo_id** | integer | required |

+ 示例

```json
{
    "subjects": [
        {
          "id": 12412412,
          "name": "Writing",
          "type": 1241,
          "weight": 1341,
        },
    ]
}
```
###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `DELETE` 删除已有的小项信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |

+ 示例

```json
{
  subjects:[{"id":2}，{"id":3}]
}
```

###### Response
```
205 Reset Content
```

## `/titleGroup`(todo)

---

## `/titleGroup/format`
`GET` `POST` `PUT` `DELETE`
### `GET` 获取大项相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。
###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | optional 列id |
| **name**        | string | optional,列名
| **lesson_id** | integer |大列所属课程id |
| **weight** | integer | optional 权重 |
###### Response
```json
{
  "subjects": [
      {
          "id": 12412412,
          "name": "Writing",
          "type": 1241,
          "weight": 1341(means 13.41),
      }
  ]
}
```

### `PUT` 更新大项相关信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |
| **name**        | string | optional |
| **lesson_id** | integer | optional |
| **weight** | integer | optional |

+ 示例

```json
{
    "subjects": [
        {
          "id": 12412412,
          "name": "Writing",
          "type": 1241,
          "weight": 1341,
        },
    ]
}
```
###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `POST` 创建新的大项信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **name**        | varchar | required |
| **weight** | integer | optional |
| **lesson_id** | integer | required |

+ 示例

```json
{
    "subjects": [
        {
          "id": 12412412,
          "name": "Writing",
          "type": 1241,
          "weight": 1341,
        },
    ]
}
```

###### Response
```
200 OK
```
失败时返回
```
400 Bad Request
```

### `DELETE` 删除已有的大项信息
###### HEAD
需要 `X-Access-Token`，携带内容为用户 token。

###### Body

| params | 类型 | 说明 |
|---|---|---|
| **id**        | integer | required |

+ 示例

```
{
  subjects:[{"id":2}，{"id":3}]
}
```

###### Response
```
205 Reset Content
```
---

## `/semester`(todo)
`GET` `PUT`
### `GET` 获取当前学期信息
### `PUT` 更改学期信息

## `/analysis`(todo)
数据分析端所需接口

## `/analysis/student` (todo)
与学生相关的接口

## `/analysis/student/name`

### `GET` 根据学生id列表获取学生姓名列表

###### HEAD
需要` X-Access-Token`，携带内容为用户 token。

###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id_list**        | list | required |

###### Response
```json
{
  "subjects": [张三, 李四]
}
```

## `/analysis/score` (todo)
与成绩相关的接口

## `/analysis/score/format`

### `GET` 根据学生id列表获取学生成绩信息

###### HEAD
需要` X-Access-Token`，携带内容为用户 token。

###### Params
| params | 类型 | 说明 |
|---|---|---|
| **id_list**        | list | required |

###### Response
```json
{
  "subjects": 
    {
      "sid": 2019212001,
      "score_mk": 79,
      "score_zz: 85,
      "score_zk: 77,
      "score_zs": 79,
      "score_ms": 80
    },
    {
      "sid": 2019212002,
      "score_mk": 69,
      "score_zz: 75,
      "score_zk: 67,
      "score_zs": 77,
      "score_ms": 70
    },
    ......
}
```

## `/analysis/score/all`

### `GET` 获取当前学期所有学生成绩信息

###### HEAD
需要` X-Access-Token`，携带内容为用户 token。

###### Params
| params | 类型 | 说明 |
|---|---|---|
| **semester** | string | required |

###### Response
```json
{
  "subjects": 
    {
      'vocabulary':40,
      'hearing':9,
      'translate':7,
      'writing':7,
      'details':7,
      'subjective_qz':20,
      'objective_qm':60,
      'subjective_qm':20,
      'xuewei':70
    },
    {
      'vocabulary':47,
      'hearing':15,
      'translate':9,
      'writing':17,
      'details':7,
      'subjective_qz':30,
      'objective_qm':72,
      'subjective_qm':30,
      'xuewei':85
    },
    ......
}
```