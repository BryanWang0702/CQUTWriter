$(function () {
    $("#summarize_submit").click(function () {
        // 获取输入值
        const inputContent = $("#summarize_input").val()
        $.ajax({
            url:"/summarize/summarize/",
            type:"post",
            data:{'inputContent': inputContent},
            dataType: 'json',
            success:function s(data) {
                //将返回的值放到对应的输入框内
                $("#summarize_abstract").val(data.abstract)
                $("#summarize_keywords").val(data.keywords)
            }
        })
    })
})