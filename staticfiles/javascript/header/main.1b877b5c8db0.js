function toggleList() {
    var list = document.getElementById("menu__usuario");
    if (list.classList.contains("hidden")) {
      showList(list);
    } else {
      hideList(list);
    }
}
  
function showList(list) {

    list.classList.remove("hidden");
    list.classList.add("visible");
    list.style.height = list.scrollHeight + "px";
    document.addEventListener("click", handleOutsideClick);
    
}
  
  function hideList(list) {
      list.style.height = "0px";

      list.addEventListener("transitionend", function() {
        
        list.classList.remove("visible");
        list.classList.add("hidden");
        document.removeEventListener("click", handleOutsideClick);

      }, {once: true});
  }
  
function handleOutsideClick(event) {

    var list        = document.getElementById("menu__usuario");
    var container   = document.getElementsByClassName("bloco__do__usuario")[0];

    if (!list.contains(event.target) && !container.contains(event.target)) {
      hideList(list);
    }
}

document.getElementById('navbar-toggle').addEventListener('click', function () {
  var menu = document.getElementById('nav__menu__principal');
  menu.classList.toggle('active');
});