// This class gets the list of free champions from the ajax call to the champion_rotation function in processor.py
// Then it loops through the returned list and gets information for each champion in the list via an ajax call to 
// champion_info in processor.py. It then adds an image, and sets its on click event listener. The on click
// event listener changes the back ground, name, and description based on the champion chosen. If there is no background
// current on the page then it adds the current champions background to the page.
function rotation(){
  $.ajax({
      type: "POST",
      url: "/champion_rotation",
      success : function(response){
        for(i = 0; i < response.info.length; i++){
          $.ajax({
              type: "POST",
              url: "/champion_info",
              data: {'id' : response.info[i]},
              success : function(data){
                var a = document.createElement("a");
                var x = document.createElement("IMG");
                x.setAttribute("src", "http://ddragon.leagueoflegends.com/cdn/6.23.1/img/champion/" + data.info[2]);
                x.setAttribute("width", "60");
                x.setAttribute("height", "60");
                a.appendChild(x);
                a.addEventListener('click', function(){changeImage(data.info);});
                document.getElementById("pics").appendChild(a);
                if (!document.body.background){
                changeImage(data.info);
                }
              }
          })
        }
      }
    })
}
