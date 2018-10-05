var dataset = [];
var array = [];

function loadDoc() {

  var n = document.getElementById('num').value;
  console.log(n);
  if (n == "") {
    alert('Please enter the number of users');
    return;
  }

  $.ajax({
    url: 'https://randomuser.me/api/?results='+n,
    dataType: 'json',
    success: function(data) {
      console.log(data);
      dataset = [];
      for (var i = 0; i < n; i++) {
      console.log(data.results[i].gender);
      array = [data.results[i].gender,data.results[i].location.postcode,data.results[i].email, data.results[i].login.username, data.results[i].phone];
      console.log(array);
      dataset.push(array);
      console.log(dataset);

    }

    $(document).ready(function() {
      $('#myTable').DataTable({
        data: dataset,
        destroy: true,
      });
    });

    }
  });
  document.getElementById('num').value = ""
}
