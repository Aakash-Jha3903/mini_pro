// auto text code js 
var typed = new Typed(".input", {
    strings:["पढ़ेगा इंडिया तभी तो बढ़ेगा इंडिया."
    ," शिक्षा का हक, छोड़ो मत!"
    ,"बेटी बचाओ बेटी पढ़ाओ"
    ,"शिक्षा करेगी नव युग का निर्माण, आने वाला समय देगा इसका प्रमाण। "],typeSpeed:45,
    backSpeed:40,
    loop:true
  });
  
  
  function startCounter(id, maxCount) {
      let count = 0;
      let interval = setInterval(function() {
        if (count < maxCount) {
          count++;
          document.getElementById(id).textContent = count + 'k+';
        } else {
          clearInterval(interval);
        }
      }, 40);
    }
  
    startCounter('number1', 60);
    startCounter('number2', 50);
    startCounter('number3', 50);
    startCounter('number4', 80);
  
  