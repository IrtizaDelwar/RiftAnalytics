function newDoc()
{
   var user = document.getElementById("searchTxt").value;
   var e = document.getElementById("region");
   var region = e.options[e.selectedIndex].text;
   if (user.length > 0){
     window.location.assign("/profile/" +  region + "/" + user)
   }
   else{
     alert("Please type a valid summoner name. Length must be between 1 and 16.")
   }
 }