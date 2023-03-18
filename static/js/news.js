$(document).ready(function () {
    $.ajax({
        url:"/news/getNews/",
        type:"post",
        data:{},
        dataType: 'json',
        success: function (data) {
            const people = data.people;
            const weibo = data.weibo;
            const zhihu = data.zhihu;
            const toutiao = data.toutiao;
            const baidu = data.baidu;
            var news;

            for (let k = 0; k < people.length; k++) {
                news = people[k];
                // 向html中插入<li>元素以增加行
                document.getElementById("people_list").innerHTML +=
                    "<li><a href='"+ news[0] +"'>"+ news[1] +"</li>"
            }

            for (let k = 0; k < toutiao.length; k++) {
                news = toutiao[k];
                // 向html中插入<li>元素以增加行
                document.getElementById("toutiao_list").innerHTML +=
                    "<li><a href='"+ news[1] +"'>"+ news[0] +"</li>"
            }
            for (let k = 0; k < baidu.length; k++) {
                news = baidu[k];
                // 向html中插入<li>元素以增加行
                document.getElementById("baidu_list").innerHTML +=
                    "<li><a href='"+ news[1] +"'>"+ news[0] +"</a><span>"+ news[2]+"</span></li>"
            }
            for (let i = 0; i < 20; i++) {
                news = weibo[i];

                // 向html中插入<li>元素以增加行
                document.getElementById("weibo_list").innerHTML +=
                    "<li><a href='"+ news[1] +"'>"+ news[0]
                    +"</a><span>"+ news[2] +"</span><span>"+ news[3] +"</span></li>"
            }

            for (let j = 0; j < 20; j++) {
                news = zhihu[j];
                document.getElementById("zhihu_list").innerHTML +=
                    "<li><a href='"+ news[1] +"'>"+ news[0]
                    +"</a><span>"+ news[2] +"</span></li>"
            }
        }
    })
})