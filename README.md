# True hosts

感谢[jianboy](https://github.com/jianboy)大佬的[源码
](https://github.com/jianboy/github-host)

## ToDo

<!-- (因为没学过Python，加上种种原因不能用电脑， 画饼ing)(其实应该挺简单的，小声bb) -->
- [ ] 优化结构(暂时搁置,没有电脑缩进太麻烦了)
- [ ] 删除多余代码
- [ ] 修复我改炸的hosts-routeros.txt
- [x] 返回多条ip
- [x] 更新ipv6版本
- [x] 遵循robots.txt
- [x] 添加冗余，自动切换源(ipv4)，可返回ipv6(防止没有结果)(已更新三源)
- [ ] 添加冗余，自动切换源(ipv6)，只返回ipv6(搁置,没有源)
- [x] tcping筛选(ipv4):尝试tcping获取的ip，如果只有低于某比例的ip不能tcping通则抛弃该ip，如果高于某比例的ip都不能tcping通则全部保留
- [ ] tcping筛选(ipv6)
