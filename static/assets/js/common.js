
AOS.init({
    duration: 1100,
    offset: 100,
    anchorPlacement: 'top-bottom'
});


$(document).ready(function(){
  $('#heroSlick').slick({
    slidesToShow: 1,           
    slidesToScroll: 1,         
    autoplay: true,            // 自動再生を有効化 
    autoplaySpeed: 5000,       // 自動再生の間隔（5000ms = 5秒）
    dots: false,               // 下のページネーションの点を非表示
    arrows: false,             // 左右の矢印を非表示
    fade: true,                // スライドをフェードで切り替える（より背景向け）
    cssEase: 'linear',         // フェード時のアニメーションをスムーズに
    pauseOnFocus: false,       // フォーカス時も自動再生を停止しない
    pauseOnHover: false        // マウスオーバー時も自動再生を停止しない
  });
});

const swiper = new Swiper('.swiper', {
  loop: true,
  effect: "fade",
  speed: 2000,
  allowTouchMove: false,

  autoplay: {
    delay: 4500, // 4.5秒ごとに切り替え
    disableOnInteraction: false,
  },
});


// 追加
let youbi_list = [7, 7, 7, 7, 7, 7, 7];
let element = document.getElementById('date-picker');
target = element.dataset.id.split(', ');
for(let i=0; i<target.length; i++){
    let val = 7;
    if(target[i] == '日'){val = 0}
    else if(target[i] == '月'){val = 1}
    else if(target[i] == '火'){val = 2}
    else if(target[i] == '水'){val = 3}
    else if(target[i] == '木'){val = 4}
    else if(target[i] == '金'){val = 5}
    else if(target[i] == '土'){val = 6}
    youbi_list[i] = val;
}

const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0');
const dd = String(today.getDate()).padStart(2, '0');
const todayString = `${yyyy}-${mm}-${dd}`; // 例: "2025-12-06"
const reservedDateInput = document.getElementById("id_reserved_date");
if (reservedDateInput) {
  flatpickr(reservedDateInput, {
    locale: "ja",
    minDate: todayString,
    dateFormat: "Y-m-d",

    // disable: [
    //         (date) => date.getDay() === youbi_list[0],
    //         (date) => date.getDay() === youbi_list[1],
    //         (date) => date.getDay() === youbi_list[2],
    //         (date) => date.getDay() === youbi_list[3],
    //         (date) => date.getDay() === youbi_list[4],
    //         (date) => date.getDay() === youbi_list[5],
    //         (date) => date.getDay() === youbi_list[6],
    //     ]
    });
}

