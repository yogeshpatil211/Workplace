
function loadDoc() {
  $.ajax({
    url: 'https://randomuser.me/api',
    dataType: 'json',
    success: function(data) {

      document.getElementById("gender").value = data.results[0].gender;
      document.getElementById("email").value = data.results[0].email;
      document.getElementById("postcode").value = data.results[0].location.postcode;
      document.getElementById("username").value = data.results[0].login.username;
      document.getElementById("phone").value = data.results[0].phone;
      document.getElementById("cell").value = data.results[0].cell;
      source = data.results[0].picture.large;
      document.getElementById("img").src=source;

    }
  });
}
