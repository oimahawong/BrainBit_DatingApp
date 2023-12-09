   
 
 let profile_Pic = document.getElementById("profilePic");
 let inputFile = document.getElementById("input-file");

 //This function switch out place holder picture
 inputFile.onchange = function(){   
     profile_Pic.src = URL.createObjectURL(inputFile.files[0]);
 }


