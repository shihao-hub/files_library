# 其他面经参考

## 1、某位同事的综面的参考资料（主管面）

1. 自我介绍
2. 软件开发流程（和软件生命周期差不多）
3. 安全有了解过吗？
4. 什么是内存泄露？怎么避免？
5. 喜欢看什么书？
6. 平时的兴趣爱好
7. 期望薪资
8. 技术栈
9. 怎么平衡家庭和工作？
10. 怎么解决压力大的问题？
11. 对于加班有什么看法？
12. 对未来什么规划？
13. 13 种加密与解密算法
14. 



# 技面问题

> 技面一二的问题应该是可以互相参考的

## 技面一

> 技术一面似乎更侧重考察八股的知识，没怎么问到项目经历

### 1、自我介绍 + 介绍项目





### 2、项目遇到的难点







### 3、Java 是否支持多继承



### 4、重写和重载





### 5、变量初始化是否是原子操作





### 6、类加载机制





### 7、try catch finally 块



### 8、ArrayList 和 LinkedList 的区别



### 9、HashMap ConcurrentHashMap 线程安全机制



### 10、进程 线程





### 11、单核 CPU 是否支持多线程





### 12、线程都有哪些状态

创建态、就绪态、运行态、阻塞态、终止态





### 13、Java 线程池的关键参数









### 14、什么是死锁、如何避免











## 技面二

> 技术二面不会侧重问太多八股，八股、项目、算法都有问到

### 1、介绍一下简历上项目的亮点和遇到的困难，是怎么去解决的





### 2、Map 接口的实现类及区别



### 3、数据库隔离级别





### 4、线程池主要参数





# 测试面经

## 1、测试流程、测试设计、测试策略、测试类型、测试方法

> 注意，这个最好背下来

### 测试流程

1. 了解用户需求

2. 参考需求规格说明书

3. 测试计划（人力物力时间进度的安排）

4. 编写测试用例

5. 评审用例

6. 搭建环境

7. 测试包安排预测（冒烟测试）

   > 冒烟测试：

8. 正式测试 - 出现 bug - 测试结束出报告

9. 版本上线

10. 面向用户



> 开发流程：
>
> 1. 了解用户需求
> 2. 进行需求分析
> 3. 得知功能组成及设计软件结构
> 4. 开发设计计划
> 5. 概要设计
> 6. 详细设计
> 7. 进行软件编写
> 8. 单元测试
> 9. 代码审查
> 10. 打包提交给测试部，测试返回 bug，更新修复 bug，再次进入测试部直到 bug 被解决
> 11. 版本上线
> 12. 面向用户使用



### 测试设计





### 测试策略

#### 单元测试

#### 集成测试

#### 确认测试

#### 系统测试

#### 验收测试

#### 回归测试



### 测试类型



### 测试方法

#### 黑盒测试

#### 白盒测试

#### 灰盒测试









## 2、黑盒测试和白盒测试的概念以及差别、白盒测试的种类以及区别







## 3、是否安装并使用过数据库，安装的数据库默认端口号是多少

MySQL：3306

MongoDB：27017

Redis：6379



## 4、Linux 常用命令有哪些

- cd
- ls
- tail、head
- mkdir
- touch
- rmdir
- rm
- cat
- vim
- systemctl
- supervisorctl



## 5、Linux 相对路径和绝对路径的含义和区别





## 6、SQL语句、对数据进行排序要用什么 SQL 语句来实现





## 7、TCP 3 次握手和 4 次挥手





## 8、Python 基础知识

- Python 数据类型
- Python 的修饰器是什么，怎么用
- 说出五个 Python 库
- 正则的贪婪匹配和懒惰匹配





## 9、性能测试是什么





## 10、测试流程有哪些，你觉得测试流程哪几个部分是比较重要的





## 11、测试的设计有哪些





## 12、app 的兼容测试



## 13、使用过的测试工具





## 其他来源问题

软件测试的基本流程（重点，面试必会）：https://www.cnblogs.com/zenghongfei/p/11597673.html

### 1、生命周期模型包含哪些阶段?你们开发的模型是什么？



### 2、测试流程包含哪些阶段？

**软件测试的基本流程（重点）**

- 测试需求分析阶段：阅读需求，理解需求，主要就是对业务的学习，分析需求点，参与需求评审会议

- 测试计划阶段：主要任务就是编写测试计划，参考软件需求规格说明书，项目总体计划，内容包括测试范围（来自需求文档），进度安排，人力物力的分配，整体测试策略的制定。风险评估与规避措施有一个制定。

- 测试设计阶段：主要是编写测试用例，会参考需求文档（原型图），概要设计，详细设计等文档，用例编写完成之后会进行评审。

- 测试执行阶段：搭建环境，执行冒烟测试（预测试）-然后进入正式测试，bug管理直到测试结束

- 测试评估阶段：出测试报告，确认是否可以上线

### 3、你们公司的开发流程是怎样的？



### 4、你们公司的测试流程是怎样的？各个阶段的输出是什么？





## Java 面经

## 1、Java 集合有哪些？

**当回答 Set 时：**

追问，Set 的组件有哪些？

>

**当回答 HashSet 时：**

追问，哈希表是更适合查询的场景还是更适合修改或删除的场景？

> 各有优势，通常最合适的是查询。
>
> 哈希表查询的平均复杂度是 O(1)
>
> 哈希表修改或删除的平均复杂度也是 O(1)，但是在极端情况下，性能可能降低而且修改或删除可能导致哈希表的重哈希。
>
> Q：重哈希啥意思？比如容量减半重新 hash？



- List：有序集合，可以包含重复元素
  - ArrayList：基于动态数组实现，支持随机存取，适合频繁读取
  - LinkedList：基于双向链表实现，适合频繁插入和删除操作
- Set：不允许重复元素的集合
  - HashSet：基于哈希表实现，提供常数时间的性能，元素无序
  - LinkedHashSet：继承自 HashSet，保证插入顺序
  - TreeSet：基于红黑树实现，元素按照自然顺序或指定比较器排序
- Map：键值对集合，键不允许重复，值可以重复
  - HashMap：基于哈希表实现，提供常数时间的性能，元素无序
  - LinkedHashMap：继承自 HashMap，保证插入顺序
  - TreeMap：基于红黑树实现，键按照自然顺序或指定比较器排序
  - Hashtable：早期的 Map 实现，线程安全，性能较 HashMap 差
- Queue：队列集合，通常用于存储待处理的元素
  - LinkedList
  - PriorityQueue：基于优先级堆实现，元素按照优先级排序
- Deque：双端队列，允许从两头插入和删除元素
  - ArrayDeque：基于动态数组实现
  - LinkedList



## 2、ArrayList 的元素有几位，扩容后是几位





## 3、SpringCloud 组件





## 4、网关阻塞







## 5、项目用了哪种数据库？

回答 MySQL 时，

面试官追问：MySQL 的索引在什么时候会失效







