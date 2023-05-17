# KOOK清水机器人开发规范

## 1.语言以及依赖

依赖:

| 类型     | 名称                                               |
| -------- | -------------------------------------------------- |
| 数据库   | MySQL                                              |
| 开发语言 | Python                                             |
| 依赖库   | `json time khl.py psutil re Mcstatus yaml MySQLdb` |

格式规范:

| 类型           | 命名格式 | 正确示范    |
| -------------- | -------- | ----------- |
| 全局变量       | 小驼峰   | `nameList`  |
| 局部变量       | 蛇底式   | `name_list` |
| 类属性         | 小驼峰   | `nameList`  |
| 类任意方法传参 | 小驼峰   | `nameList`  |
| 类名           | 大驼峰   | `NameList`  |
| 类成员方法     | 小驼峰   | `nameList`  |
| 类方法         | 小驼峰   | `nameList`  |
| 类静态方法     | 小驼峰   | `nameList`  |

**注意事项：**

1. 请不要写单独方法，请把方法封装进类，尽量写成可重复使用的轮子

2. 请写出类文档和方法文档注释，必须写出类型注释(必须是中文) (格式规范见下文)

3. 无论是哪里的变量，必须给出变量类型（如找到未知变量类型，请自行请求后写出）

4. 所有传参必须按照此格式编写 `变量名: 变量类型=默认值` 如果默认值没有特定规范请默认为None

5. 请在调用函数/方法时明确传参，声明传参对应的值 例: `nameList(name="Jack", age=12)`
