 function generator()
 {
   var championID = ['266', '103', '84', '12', '32', '34', '1', '22', '136', '268', '432', '53', '63', '201', '51', '69', '31', '42', '122', '131', '119', '36', '245', '60', '28', '81', '9', '114', '105', '3', '41', '86', '150', '79', '104', '120', '74', '420', '39', '427', '40', '59', '24', '126', '202', '222', '429', '43', '30', '38', '55', '10', '85', '121', '203', '240', '96', '7', '64', '89', '127', '236', '117', '99', '54', '90', '57', '11', '21', '62', '82', '25', '267', '75', '111', '76', '56', '20', '2', '61', '80', '78', '133', '33', '421', '58', '107', '92', '68', '13', '113', '35', '98', '102', '27', '14', '15', '72', '37', '16', '50', '134', '223', '163', '91', '44', '17', '412', '18', '48', '23', '4', '29', '77', '6', '110', '67', '45', '161', '254', '112', '8', '106', '19', '101', '5', '157', '83', '154', '238', '115', '26', '143']
   var bootID = ['3006', '3009', '3020', '3047', '3111', '3117', '3158']
   var itemID = ['3001', '3504', '3174', '3060', '3102', '3153', '3742', '3812', '3147', '3814', '3508', '3092', '3110', '3022', '3026', '3124', '3030', '3146', '3152', '3025', '3031', '3109', '3151', '3100', '3190', '3036', '3285', '3156', '3041', '3139', '3222', '3165', '3033', '3042', '3115', '3056', '3046', '3089', '3143', '3094', '3074', '3107', '3800', '3027', '2045', '3085', '3116', '3040', '3065', '3087', '3053', '3068', '3071', '3072', '3075', '3748', '3078', '3135', '3083', '3091', '3142', '3050', '3157', '3512']
   var summonerID = ['21', '1', '14', '3', '4', '6', '7', '13', '11', '12']

   var champion = championID[Math.floor(Math.random() * championID.length)];
   $.ajax({
     type: "POST",
     url: "/champion_info",
     data: {'id' : champion},
     success : function(response){
       document.getElementById("generated-champion-image").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/champion/" + response.info[2] + ">";
       document.getElementById("generated-champion").innerHTML = response.info[0];
       document.getElementById("generated-champion-description").innerHTML = response.info[1];
     }
   })

   var summoner1 = summonerID[Math.floor(Math.random() * summonerID.length)];
   var summoner2 = summonerID[Math.floor(Math.random() * summonerID.length)];
   while (summoner1 == summoner2){
     summoner2 = summonerID[Math.floor(Math.random() * summonerID.length)];
    }
   $.ajax({
     type: "POST",
     url: "/sspell_info",
     data: {'id' : summoner1, 'id2' : summoner2},
     success : function(response){
       document.getElementById("generated-ss1").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/spell/" + response.info[1] + ">" + "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/spell/" + response.info2[1] + "> <p>" + response.info[0] + " & " + response.info2[0] + "</p>";
     }
   })

   var boot = bootID[Math.floor(Math.random() * bootID.length)];
   $.ajax({
     type: "POST",
     url: "/item_info",
     data: {'id' : boot},
     success : function(response){
       document.getElementById("generated-boot").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/item/" + response.info[1] + "> <p>" + response.info[0] + "</p>";
     }
   })

   var item1 = itemID[Math.floor(Math.random() * itemID.length)];
   $.ajax({
     type: "POST",
     url: "/item_info",
     data: {'id' : item1},
     success : function(response){
       document.getElementById("generated-item1").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/item/" + response.info[1] + "> <p>" + response.info[0] + "</p>";
     }
   })

   var item2 = itemID[Math.floor(Math.random() * itemID.length)];
   $.ajax({
     type: "POST",
     url: "/item_info",
     data: {'id' : item2},
     success : function(response){
       document.getElementById("generated-item2").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/item/" + response.info[1] + "> <p>" + response.info[0] + "</p>";
     }
   })

   var item3 = itemID[Math.floor(Math.random() * itemID.length)];
   $.ajax({
     type: "POST",
     url: "/item_info",
     data: {'id' : item3},
     success : function(response){
       document.getElementById("generated-item3").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/item/" + response.info[1] + "> <p>" + response.info[0] + "</p>";
     }
   })

   var item4 = itemID[Math.floor(Math.random() * itemID.length)];
   $.ajax({
     type: "POST",
     url: "/item_info",
     data: {'id' : item4},
     success : function(response){
       document.getElementById("generated-item4").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/item/" + response.info[1] + "> <p>" + response.info[0] + "</p>";
     }
   })

   var item5 = itemID[Math.floor(Math.random() * itemID.length)];
   $.ajax({
     type: "POST",
     url: "/item_info",
     data: {'id' : item5},
     success : function(response){
       document.getElementById("generated-item5").innerHTML = "<img src =http://ddragon.leagueoflegends.com/cdn/6.23.1/img/item/" + response.info[1] + "> <p>" + response.info[0] + "</p>";
     }
   })
}