document.addEventListener("DOMContentLoaded", function () {
    let backgroundSlider = document.getElementById("bg");
    let images = [
        '/static/img/image1.jpg',
        '/static/img/image2.jpg',
        '/static/img/image3.jpg'
    ];
    let index = 0;

    function changeBackground() {
        // 正确使用 url() 函数
        backgroundSlider.style.backgroundImage = 'url(' + images[index] + ')';
        index = (index + 1) % images.length; // 循环播放
    }

    // 初始化背景图片
    changeBackground();

    // 每3000毫秒（3秒）轮换一次背景图片
    setInterval(changeBackground, 3000);
});