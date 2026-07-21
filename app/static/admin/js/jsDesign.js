
    function validateEmail(paramEmailID) {
      var filter = /^[0-9a-z.]+\@[a-z0-9]+\.[a-zA-z0-9]{2,4}$/;
      
      if (filter.test(paramEmailID)) {
        return true;
      } else {
        return false;
      }
    }

    

$("#btn_add").click(function (e) {
  if ($("#selDesignType").val().trim().length < 1) {
    snackbar_error("Please Select Design Type");
    $("#selDesignType").focus();
    return false;
  }

  if ($("#filePhoto").val().trim().length < 1) {
    snackbar_error("Please Select Photo");
    $("#filePhoto").focus();
    return false;
  }

  var formData = new FormData();
  
    formData.append("selDesignType", $("#selDesignType").val());
    let lclFile = document.getElementById("filePhoto");
    lclFile1 = lclFile.files[0];
    formData.append("filePhoto", lclFile1);
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());
    formData.append("action", "add");

  $.ajax({
    beforeSend: function () {
      $(".btn .spinner-border").show();
      $("#btn_add").attr("disabled", true);
    },
    url: "/admin_design_details/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (result) {

      snackbar_success("Details Added Successfully");
      location.reload();
      $("#add_modal").modal('hide');
      
    },
    error: function (request, error) {
      console.error(error);
    },
    complete: function () {
      $(".btn .spinner-border").hide();
      $("#btn_add").attr("disabled", false);
    },
  });
});
$(document).ready(function () {

  $(document).on("click", "#btn_update", function () {

    if ($("#txtName1").val().trim().length < 1) {
    snackbar_error("Please Enter Name");
    $("#txtName1").focus();
    return false;
  }

  if ($("#filePhoto1").val().trim().length < 1) {
    snackbar_error("Please Select Photo1");
    $("#filePhoto").focus();
    return false;
  }

  var formData = new FormData();
  
    formData.append("txtName1", $("#txtName1").val());
    formData.append("txtDescription1", $("#txtDescription1").val());
    let lclFile = document.getElementById("filePhoto1");
    formData.append("id", $("#edit_id").val());
    lclFile1 = lclFile.files[0];
    formData.append("filePhoto1", lclFile1);
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());
    formData.append("action", "add");

  $.ajax({
    beforeSend: function () {
      $(".btn .spinner-border").show();
      $("#btn_update").attr("disabled", true);
    },
    url: "/admin_design_details_create/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (result) {

      snackbar_success("Details Created Successfully");
      location.reload();
      $("#edit_modal").modal('hide');
      
    },
    error: function (request, error) {
      console.error(error);
    },
    complete: function () {
      $(".btn .spinner-border").hide();
      $("#btn_update").attr("disabled", false);
    },
  });
  });

  $(document).on("click", "#btn_delete", function () {

    var formData = new FormData();
    formData.append("id", $("#delete_id").val());
    formData.append("action", "delete");
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());
    $.ajax({
      beforeSend: function () {
        $(".btn .spinner-border").show();
      },

      url: "/admin_design_details/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function () {
        snackbar_success("Details deleted succesfully");
        location.reload();
        $("#delete_modal").modal('hide');
      },
      error: function (request, error) {
        console.error(error);
      },
      complete: function () {
        $(".btn .spinner-border").hide();
        $(".close").click();
      },
    });
  });

  $(document).on("click", "#btn_delete1", function () {

    var formData = new FormData();
    formData.append("id", $("#delete_id1").val());
    formData.append("action", "delete");
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());
    $.ajax({
      beforeSend: function () {
        $(".btn .spinner-border").show();
      },

      url: "/admin_design_details_create/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function () {
        snackbar_success("Details deleted succesfully");
        location.reload();
        $("#delete_modal").modal('hide');
      },
      error: function (request, error) {
        console.error(error);
      },
      complete: function () {
        $(".btn .spinner-border").hide();
        $(".close").click();
      },
    });
  });

  $(document).on("click", "#add_user", function () {

    $("#txtName").val('');
    $("#txtEmail").val('');
    $("#txtMobileNo").val('');
    $("#txtPassword").val('');

  });
});
getAdminData();

function getAdminData() {

  var formData = new FormData();
  formData.append("action", "getData");
  formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

  $.ajax({

      url: "/admin_design_details/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#tableData tr:gt(0)").remove();
        for(var i = 0; i < response.length; i++) {
            let img = response[i].de_image.substring(3);
          var j = i + 1;
          $("#tableData").append('<tr><td>'+j+'</td><td style="display: none;">'+response[i].de_id+'</td><td>'+response[i].de_name+'</td><td><img src='+img+' height="100"></td><td><div class="d-flex" style="justify-content: space-evenly;"><a href="javascript:void(0);" id="edit_row" title="View/Edit" data-toggle="modal" data-target="#edit_modal" class="text-primary" onClick="getRowsUpdate();"> <i class="fas fa-eye"></i></a><a href="javascript:void(0);" title="Delete" data-toggle="modal" data-target="#delete_modal" class="text-danger" id="delete_row" onClick="getRowsDelete();"> <i class="far fa-trash-alt"></i></a></div></td></tr>');
        }
      },
      error: function (request, error) {
        console.error(error);
      },
      complete: function () {

      },
    });

}

function getData(id) {

  var formData = new FormData();
  formData.append("action", "getData");
  formData.append("id", id);
  formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

  $.ajax({

      url: "/admin_design_details_create/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#tableData1 tr:gt(0)").remove();
        for(var i = 0; i < response.length; i++) {
            let img = response[i].ar_image.substring(3);
          var j = i + 1;
          $("#tableData1").append('<tr><td>'+j+'</td><td style="display: none;">'+response[i].ar_id+'</td><td>'+response[i].ar_name+'</td><td><img src='+img+' height="100"></td><td>'+response[i].ar_description+'</td><td><div class="d-flex" style="justify-content: space-evenly;"><a href="javascript:void(0);" title="Delete" data-toggle="modal" data-target="#delete_modal1" class="text-danger" id="delete_row" onClick="getRowsDelete1();"> <i class="far fa-trash-alt"></i></a></div></td></tr>');
        }
      },
      error: function (request, error) {
        console.error(error);
      },
      complete: function () {

      },
    });

}



function getRowsUpdate() {
  $("#tableData tr").click(function() {
      var currentRow = $(this).closest("tr");
      var lclID = currentRow.find("td:eq(1)").text();
      
      $("#edit_id").val(lclID);
      getData(lclID);

  });
}


function getRowsDelete() {
  $("#tableData tr").click(function() {
      var currentRow = $(this).closest("tr");
      var lclID = currentRow.find("td:eq(1)").text();
      $("#delete_id").val(lclID);

  });
}
function getRowsDelete1() {
  $("#tableData1 tr").click(function() {
      var currentRow = $(this).closest("tr");
      var lclID = currentRow.find("td:eq(1)").text();
      $("#delete_id1").val(lclID);

  });
}