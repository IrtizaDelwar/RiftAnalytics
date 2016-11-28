function changeImage(champ){
  if (document.body){
    champ[0] = champ[0].replace(/\s+/g, '');
    string = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + champ[0] + "_0.jpg";
    document.body.background = string;
    document.getElementById("name").innerHTML = champ[0];
    document.getElementById("desc").innerHTML = champ[1];
  }
}