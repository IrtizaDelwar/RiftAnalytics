// This script takes the username and region from the searchbox in the top right corner of the web page
// and passes that info to the profile function in processor.py that loads the profile page.
// This function also checks that the user entered a username, and if not then it returns an alert.
// Also the search box itself makes sures that the username is no larger than 16 characters.
function newDoc()
{
   var user = document.getElementById("searchTxt").value;
   var e = document.getElementById("region");
   var region = e.options[e.selectedIndex].text;
   if (user.length > 0){ //Make sure a username was passed in
     window.location.assign("/profile/" +  region + "/" + user)
   }
   else{
     alert("Please type a valid summoner name. Length must be between 1 and 16.")
   }
 }