$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#IranMap .list').height();
        var width = $('#IranMap .list').width();
        if (height > width) {
            $('#IranMap svg').height(width).width(width);
        } else {
            $('#IranMap svg').height(height).width(height);
        }
    }
    resposive();

    $('#IranMap svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#IranMap .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#IranMap .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#IranMap .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#IranMap .list a').removeClass('hover');
        $('#IranMap .show-title').html('').css({'display': 'none'});
    });

    $('#IranMap .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#IranMap svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#IranMap svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#IranMap').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#IranMap .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#IranMap .show-title').css({'left': x, 'top': y});
        }
    });

});


// herbal IranMap

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#herbal-IranMap .list').height();
        var width = $('#herbal-IranMap .list').width();
        if (height > width) {
            $('#herbal-IranMap svg').height(width).width(width);
        } else {
            $('#herbal-IranMap svg').height(height).width(height);
        }
    }
    resposive();

    $('#herbal-IranMap svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#herbal-IranMap .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#herbal-IranMap .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#herbal-IranMap .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#herbal-IranMap .list a').removeClass('hover');
        $('#herbal-IranMap .show-title').html('').css({'display': 'none'});
    });

    $('#herbal-IranMap .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#herbal-IranMap svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#herbal-IranMap svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#herbal-IranMap').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#herbal-IranMap .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#herbal-IranMap .show-title').css({'left': x, 'top': y});
        }
    });

});


// disease IranMap

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#disease-IranMap .list').height();
        var width = $('#disease-IranMap .list').width();
        if (height > width) {
            $('#disease-IranMap svg').height(width).width(width);
        } else {
            $('#disease-IranMap svg').height(height).width(height);
        }
    }
    resposive();

    $('#disease-IranMap svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#disease-IranMap .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#disease-IranMap .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#disease-IranMap .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#disease-IranMap .list a').removeClass('hover');
        $('#disease-IranMap .show-title').html('').css({'display': 'none'});
    });

    $('#disease-IranMap .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#disease-IranMap svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#disease-IranMap svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#disease-IranMap').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#disease-IranMap .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#disease-IranMap .show-title').css({'left': x, 'top': y});
        }
    });

});


// khorasan razavi

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#khorasan-razavi-map .list').height();
        var width = $('#khorasan-razavi-map .list').width();
        if (height > width) {
            $('#khorasan-razavi-map svg').height(width).width(width);
        } else {
            $('#khorasan-razavi-map svg').height(height).width(height);
        }
    }
    resposive();

    $('#khorasan-razavi-map svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#khorasan-razavi-map .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#khorasan-razavi-map .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#khorasan-razavi-map .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#khorasan-razavi-map .list a').removeClass('hover');
        $('#khorasan-razavi-map .show-title').html('').css({'display': 'none'});
    });

    $('#khorasan-razavi-map .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#khorasan-razavi-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#khorasan-razavi-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#khorasan-razavi-map').mousemove(function(e) {
        // var posx = 0;
        // var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#khorasan-razavi-map .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#khorasan-razavi-map .show-title').css({'left': x, 'top': y});
        }
    });

});



// qazvin

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#qazvin-map .list').height();
        var width = $('#qazvin-map .list').width();
        if (height > width) {
            $('#qazvin-map svg').height(width).width(width);
        } else {
            $('#qazvin-map svg').height(height).width(height);
        }
    }
    resposive();

    $('#qazvin-map svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#qazvin-map .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#qazvin-map .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#qazvin-map .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#qazvin-map .list a').removeClass('hover');
        $('#qazvin-map .show-title').html('').css({'display': 'none'});
    });

    $('#qazvin-map .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#qazvin-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#qazvin-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#qazvin-map').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#qazvin-map .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#qazvin-map .show-title').css({'left': x, 'top': y});
        }
    });

});



// hamadan

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#hamadan-map .list').height();
        var width = $('#hamadan-map .list').width();
        if (height > width) {
            $('#hamadan-map svg').height(width).width(width);
        } else {
            $('#hamadan-map svg').height(height).width(height);
        }
    }
    resposive();

    $('#hamadan-map svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#hamadan-map .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#hamadan-map .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#hamadan-map .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#hamadan-map .list a').removeClass('hover');
        $('#hamadan-map .show-title').html('').css({'display': 'none'});
    });

    $('#hamadan-map .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#hamadan-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#hamadan-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#hamadan-map').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#hamadan-map .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#hamadan-map .show-title').css({'left': x, 'top': y});
        }
    });

});



// ardabil

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#ardabil-map .list').height();
        var width = $('#ardabil-map .list').width();
        if (height > width) {
            $('#ardabil-map svg').height(width).width(width);
        } else {
            $('#ardabil-map svg').height(height).width(height);
        }
    }
    resposive();

    $('#ardabil-map svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#ardabil-map .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#ardabil-map .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#ardabil-map .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#ardabil-map .list a').removeClass('hover');
        $('#ardabil-map .show-title').html('').css({'display': 'none'});
    });

    $('#ardabil-map .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#ardabil-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#ardabil-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#ardabil-map').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#ardabil-map .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#ardabil-map .show-title').css({'left': x, 'top': y});
        }
    });

});


// golestan

$(function() {

    $(window).resize(function() {
        resposive();
    });

    function resposive() {
        var height = $('#golestan-map .list').height();
        var width = $('#golestan-map .list').width();
        if (height > width) {
            $('#golestan-map svg').height(width).width(width);
        } else {
            $('#golestan-map svg').height(height).width(height);
        }
    }
    resposive();

    $('#golestan-map svg g a path').hover(function() {
        var className = $(this).attr('class');
        var parrentClassName = $('a').parent('g').attr('class');
        var itemName = $('#golestan-map .list .' + parrentClassName + ' .' + className + ' a').html();
        if (itemName) {
            $('#golestan-map .list .' + parrentClassName + ' .' + className + ' a').addClass('hover');
            $('#golestan-map .show-title').html(itemName).css({'display': 'block'});
        }
    }, function() {
        $('#golestan-map .list a').removeClass('hover');
        $('#golestan-map .show-title').html('').css({'display': 'none'});
    });

    $('#golestan-map .list ul li ul li a').hover(function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#golestan-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass + ' hover');
    }, function() {
        var className = $(this).parent('li').attr('class');
        var parrentClassName = $(this).parent('li').parent('ul').parent('li').attr('class');
        var object = '#golestan-map svg g.' + parrentClassName + ' path.' + className;
        var currentClass = $(object).attr('class');
        $(object).attr('class', currentClass.replace(' hover', ''));
    });

    $('#golestan-map').mousemove(function(e) {
        var posx = 0;
        var posy = 0;
        if (!e)
            var e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        if ($('#golestan-map .show-title').html()) {
            var offset = $(this).offset();
            var x = (posx - offset.left + 25) + 'px';
            var y = (posy - offset.top - 5) + 'px';
            $('#golestan-map .show-title').css({'left': x, 'top': y});
        }
    });

});
