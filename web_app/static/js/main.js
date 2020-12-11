$(document).ready(function() {
  $(".dropdown-toggle").dropdown();

  if(window.location.pathname == "/create_league") {
    document.getElementById('extra-user').onclick = duplicate;
    document.getElementById('remove-user').onclick = remove;
    var i = 0;
    var original = document.getElementById('add-users0');
  }
  if(window.location.pathname == "/manage_league") {
    var lg = document.getElementById('sel-league');
    document.getElementById('add-users0');
  }
  function duplicate() {
    var og = document.getElementById('add-users'+i);
    var clone = og.cloneNode(true); // "deep" clone      
    var inner_id = clone.getElementsByClassName("form-control username")[0];
    inner_id.value="";
    console.log(inner_id);
    clone.id = "add-users" + ++i; // there can only be one element with an ID
    clone.value="";
    og.parentNode.appendChild(clone);
    edit_names(i)
    document.getElementById('submit').value=i;
  }

  function remove() {
    if(i != 0) {
      var og = document.getElementById('add-users'+i);
      og.parentElement.removeChild(og);
      --i;
    }
  }
  function edit_names(i) {
    var input_controls = document.getElementById('add-users'+i).getElementsByClassName('form-control');
    var input_checkboxes = document.getElementById('add-users'+i).getElementsByClassName('form-check-input');
    for(j = 0; j < 2; j++) {
      input_controls[j].name = input_controls[j].name.substring(0, input_controls[j].name.length - 1) + i
      input_checkboxes[j].name = input_checkboxes[j].name.substring(0, input_checkboxes[j].name.length - 1) + i
    }
  }
});