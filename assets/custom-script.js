window.setInterval(function(){
  var x = document.getElementById("wordcontainer").querySelectorAll("div");
  var y = document.getElementById("piecontainer").querySelectorAll("div");

for (i = 0; i < x.length; i++) {
	if (i >0){
         x[i].style.borderTop = "1px solid black";
	}
  x[i].style.fontWeight  = "bold";
  x[i].style.fontSize  = "25px";

  y[i].style.fontWeight  = "bold";
  y[i].style.fontSize  = "25px";
  y[i].style.marginLeft  = "13px";
}

}, 1000);