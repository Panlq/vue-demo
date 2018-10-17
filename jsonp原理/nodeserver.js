const http = require("http");

const urlModule = require("url");

const server = http.createServer();

// 监听 服务器的 request 请求事件 处理每个请求
server.on("request", (req, res) => {
    const url = req.url;
    // 解析客户端请求的URL地址, 截取parse部分, true表示用query方法
    var info = urlModule.parse(url, true);

    if (info.pathname === "/getjsonp") {
        // 获取客户端要返回给客户端的数据对象
        var cbName = info.query.callback;
        // 手动拼接数据返回给客户端的数据对象
        var data = {
            name: "xfj",
            age: 22,
            gender: "man",
            job: 'python'
        }

        var result = `${cbName}(${JSON.stringify(data)})`;
        // 将拼接好的方法的调用, 返回给客户端解析执行
        res.end(result);
    } else {
        res.end("404");
    }
});

server.listen("3000", () => {
    console.log("server runing at http://127.0.0.1:3000");
})