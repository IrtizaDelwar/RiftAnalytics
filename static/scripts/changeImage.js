// Changes the background image of the html page for free champ rotation.
// When one of the portraits for the free champ rotation is clicked, this script
// changes the background image, and the name/description of the champion.
function changeImage(champ){
  if (document.body){
    champ[0] = champ[0].replace(/\s+/g, '');
    string = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + champ[0] + "_0.jpg";
    document.body.background = string;
    document.getElementById("name").innerHTML = champ[0];
    document.getElementById("desc").innerHTML = champ[1];
  }
}