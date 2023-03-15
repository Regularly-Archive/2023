本项目用于演示 Nginx 部署前端项目时，反向代理路由与前端相对地址(publicPath) 之间的关系：

* with-baseurl：应用2 直接放到应用1 下面，应用2 通过 www.abc.com/app2/ 访问
* with-multiple-sites：应用1 和 应用2，属于两个独立的站点，应用 2 通过 www.abc.com/app2/ 访问

除此以外，还可以考虑在 Nginx 中使用相同域名不同端口、不同域名不同端口的形式来解决此类问题，以上。