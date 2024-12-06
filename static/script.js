

/* Funskjon for søkeknapp */

let slideSearch = document.querySelector(".searchbutton");

function showBar() {
  if (slideSearch.style.display === "block") {
    slideSearch.style.display = "none";
  } else {
    slideSearch.style.display = "block";
  }
}

window.onload = function(){
document.getElementById('loading').className = 'loading active';
setTimeout(function(){
  document.getElementById('loading').style.display='none';
},3000)
}

/* Funksjon for søkeknapp end */