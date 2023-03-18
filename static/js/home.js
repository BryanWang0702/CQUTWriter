$(function () {
    $("#home_submit").click(function () {
        // 点击过后将该按钮禁用
        const bt = document.getElementById("home_submit");
        bt.disabled = true;
        bt.innerText = "正在生成中...";
        // 获取输入值
        var title = $("#home_title").val()
        var sentence = $("#home_output").val()
        $.ajax({
            url:"/home/generate/",
            type:"post",
            data:{'title': title, 'sentence': sentence},
            dataType: 'json',
            success:function s(data) {
                //将返回的值放到对应的输入框内
                $("#home_output").val(data.outputContent)
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "生成";
            },
            error:function () {
                $("#home_output").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "生成";
            }
        })
    })
})