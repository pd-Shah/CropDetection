
// map modal

window.onload = function () {
    $(function () {
        var modal = document.getElementById('khorasan-razavi-modal');

        var img = document.getElementById('khorasan-razavi-map');
        var modalImg = document.getElementById("khorasan-razavi-map");
        var captionText = document.getElementById("caption");
        img.onclick = function () {
            modal.style.display = "block";
            // modalImg.src = this.src;
            captionText.innerHTML = "خراسان رضوی";
        }

        var span = document.getElementsByClassName("khorasan-razavi-close")[0];

        span.onclick = function () {
            modal.style.display = "none";
        }
    });


    $(function () {
        var modal = document.getElementById('qazvin-modal');

        var img = document.getElementById('qazvin-map');
        var modalImg = document.getElementById("qazvin-img");
        var captionText = document.getElementById("caption");
        img.onclick = function () {
            modal.style.display = "block";
            // modalImg.src = this.src;
            captionText.innerHTML = "قزوین";
        }

        var span = document.getElementsByClassName("qazvin-close")[0];

        span.onclick = function () {
            modal.style.display = "none";
        }
    });


    $(function () {
        var modal = document.getElementById('hamadan-modal');

        var img = document.getElementById('hamadan-map');
        var modalImg = document.getElementById("hamadan-img");
        var captionText = document.getElementById("caption");
        img.onclick = function () {
            modal.style.display = "block";
            // modalImg.src = this.src;
            captionText.innerHTML = " همدان";
        }

        var span = document.getElementsByClassName("hamadan-close")[0];

        span.onclick = function () {
            modal.style.display = "none";
        }
    });


    $(function () {
        var modal = document.getElementById('ardabil-modal');

        var img = document.getElementById('ardabil-map');
        var modalImg = document.getElementById("ardabil-img");
        var captionText = document.getElementById("caption");
        img.onclick = function () {
            modal.style.display = "block";
            // modalImg.src = this.src;
            captionText.innerHTML = " همدان";
        }

        var span = document.getElementsByClassName("ardabil-close")[0];

        span.onclick = function () {
            modal.style.display = "none";
        }
    });


    $(function () {
        var modal = document.getElementById('golestan-modal');

        var img = document.getElementById('golestan-map');
        var modalImg = document.getElementById("golestan-img");
        var captionText = document.getElementById("caption");
        img.onclick = function () {
            modal.style.display = "block";
            // modalImg.src = this.src;
            captionText.innerHTML = " همدان";
        }

        var span = document.getElementsByClassName("golestan-close")[0];

        span.onclick = function () {
            modal.style.display = "none";
        }
    });
};


$(function () {
    $('.owl-carousel').owlCarousel({
        rtl:true,
        loop: true,
        margin: 10,
        nav: true,
        items: 1,
        navText: ["<span class='ol-pre'>قبلی</span>", "<span class='ol-nxt'>بعدی</span>", "", ""]
    })
});