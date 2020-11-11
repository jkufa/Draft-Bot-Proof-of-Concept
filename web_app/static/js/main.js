$(document).ready(function() {
  $(".dropdown-toggle").dropdown();

  if(window.location.pathname == "/create_league") {
    document.getElementById('extra-user').onclick = duplicate;
    var i = 0;
    var original = document.getElementById('add-users0');
  }
  function duplicate() {
      var clone = original.cloneNode(true); // "deep" clone      
      clone.id = "add-users" + ++i; // there can only be one element with an ID
      original.parentNode.appendChild(clone);
      edit_names(i);
      var p = {'p':i};
      console.log(p);
  }
  function edit_names(i) {
    var input_controls = document.getElementById('add-users'+i).getElementsByClassName('form-control');
    var input_checkboxes = document.getElementById('add-users'+i).getElementsByClassName('form-check-input');
    for(j = 0; j < 2; j++) {
      input_controls[j].name = input_controls[j].name.substring(0, input_controls[j].name.length - 1) + i
      input_checkboxes[j].name = input_checkboxes[j].name.substring(0, input_checkboxes[j].name.length - 1) + i
    }
  }

  $('#submit').click(function() {
    console.log("run");
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "{{url_for('/create_league')}}",
      traditional: "true",
      data: JSON.stringify({hello: "world"}),
      dataType: "json",
      success: function(response) {
        console.log("success");
      },
      error: function(err) {
        console.log(err);
      }
    });
  });
});