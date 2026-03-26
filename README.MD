# PicACG-Viewer

## 简介

使用Python，基于[Kivy](https://github.com/kivy/kivy)，并使用本人的[picaapi](https://github.com/TalkDeBPD/picaapi)库，开发的哔咔漫画客户端。

作者计划择机将全部项目改用Java/Kotlin开发。

## 功能

- [x] 自动登录
- [ ] 注册
- [x] 搜索漫画、查看分类
- [ ] 查看排行榜
- [x] 查看漫画信息
- [x] 阅读漫画
- [ ] 查看并发送评论
- [ ] 查看个人信息
- [ ] 查看个人收藏列表
- [ ] 修改个人信息
- [ ] 下载漫画
- [ ] 游戏区

## 自行构建的注意事项

* 由于Kivy在开发状态下，默认字体Roboto无法正常显示中文，故借助了思源黑体。
* 由于Buildozer构建时Pyjnius和Kivy源码中使用了旧版Python的long类型导致报错，<del>我准备了补丁文件便于大家修改源码中的错误</del>。
* 本源码可能包含：
* * 稀烂的文件结构；
* * 支离破碎的load方法；
* * 被不小心吃掉的except。
