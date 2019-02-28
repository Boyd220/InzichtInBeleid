var once = false;
window.setInterval(function(){
  if(document.getElementById("piecontainer") != null){
      var y = document.getElementById("piecontainer").querySelectorAll(".Pietitles");

    for (i = 0; i < y.length; i++) {
      if(once==false)
      {
        y[i].innerHTML = 'V: ' + y[i].innerHTML.replace('?', '?<br/>A:');      
      }
    }
    once = true;
  }
}, 1000);