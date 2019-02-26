window.setInterval(function(){
  var x = document.getElementById("wordcontainer").querySelectorAll("div");
console.log(x);

for (i = 0; i < x.length; i++) {
	if (i >0){
		 //x[i].style.marginTop = "1em";
		 x[i].style.borderTop = "1px solid black"; 
	}
  x[i].style.fontWeight  = "bold";
  x[i].style.fontSize  = "25px";
}

}, 1000);