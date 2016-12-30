// For truncating all categories
jQuery(function () {

    var minimized_elements = $('p.card-text');

    minimized_elements.each(function () {
        var t = $(this).text();
        if (t.length < 100) return;

        $(this).html(
            t.slice(0, 100) + '<span>... </span><a href="#" class="more">More</a>' +
            '<span style="display:none;">' + t.slice(100, t.length) + ' <a href="#" class="less">Less</a></span>'
        );

    });

    $('a.more', minimized_elements).click(function (event) {
        event.preventDefault();
        $(this).hide().prev().hide();
        $(this).next().show();
    });

    $('a.less', minimized_elements).click(function (event) {
        event.preventDefault();
        $(this).parent().hide().prev().show().prev().show();
    });

});