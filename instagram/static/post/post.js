window.onscroll = function() {myFunction()};

function myFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        document.getElementById("insta-head").className = "header header-scrolled";
        document.getElementById("insta-head-wrapper").className = "header-wrapper wrapper-scrolled";
        document.getElementById("insta-logo").style.height="0px";
    } else {
        document.getElementById("insta-head").className = "header";
        document.getElementById("insta-head-wrapper").className = "header-wrapper";
        document.getElementById("insta-logo").style.height="40px";
    }
};



