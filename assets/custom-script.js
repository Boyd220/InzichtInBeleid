function ChangeNames(){
var maximum = 5


        var a = document.getElementsByClassName('dash-header');
        console.log(a);
        for (var i = 1; i < maximum; i++) {
            console.log(a[i]);
        }

        Array.prototype.forEach.call(a, function(el) {
            // Do stuff here
            console.log(el);
        });

}

ChangeNames();
