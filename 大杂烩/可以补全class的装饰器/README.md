
[dataclasses的官方文档](https://docs.python.org/zh-cn/3.9/library/dataclasses.html?highlight=dataclasses#module-dataclasses)
# $ummary   

+ dataclasses库是可节省写模板代码（一个装饰器即可隐式地将一个class补全、补完整）的工作。   
+ attr库是第三方库，基于dataclasses库，所做工作在本质上相同，只是名称略有不同。attr支持slots   
+ @functools.total_ordering 能实现 @dataclasses.dataclass 的部分功能 —— 用于全比较的magic方法，但是有些慢，不如手动补上这些代码。   
+ inspect.getmembers(obj, inspect.isfunction)可查看该 object 里的所有成员，包括属性、方法和magic方法。[inspect](https://docs.python.org/zh-cn/3.9/library/inspect.html?highlight=inspect#module-inspect "python官方文档")   
   

# 举例：   
1评论类，2重写python的数据结构   

写一个class时，除了主要的功能方法外，还需要写许多special 方法，如__eq__、__repr__甚至是__hash__（实现了就能放进dict里）等，dataclasses库的@dataclass和functools库的@total_ordering都会自动补全__le__,__gt__等这些用于全比较的special方法。但是@total_ordering运行有些慢，不如手动补上这些代码。   

## @dataclasses.dataclass(frozen=True, order=True)   
默认自动补上__init__、__repr__、__eq__这三个基础的special方法。   

1. frozen=True将使实例属性immutable（不可变），这将补上__hash__、__setattr__两个special方法。哈希了就不可变了   

2. order=True将补全用于全比较的所有方法。（total_ordering干的就是这件事）。   

3. field进一步对class中的实例属性加工，如compare=False阻止比较，hash=False不可哈希，repr=False不可打印   

可通过dataclasses.replace(obj, attr_of_obj=xx）修改不可变属性的值   

## @attr.s(frozen=True, order=True)   
