function getData() {
    const formData = new FormData();
    formData.append("action", "getData");
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

    $.ajax({
        url: "/get_tailor_bookings/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $("#tableData tbody").empty();

            response.forEach(function (item, index) {
                const slNo = index + 1;

                const rowHtml = `
                    <tr>
                        <td>${slNo}</td>
                        <td style="display: none;">${item.bk_id}</td>
                        <td>${item.user_email}</td>
                        <td>${item.de_name}</td>
                        <td>${item.booking_date}</td>
                        <td>${item.booking_time}</td>
                        <td>${item.status}</td>
                        <td><div class="d-flex" style="justify-content: space-evenly;"><a href="javascript:void(0);" id="edit_row" title="View/Edit" data-toggle="modal" data-target="#edit_modal" class="text-primary" onClick="getRowsUpdate();"> <i class="fas fa-pen"></i></a><a href="javascript:void(0);" title="View" data-toggle="modal" data-target="#view_modal" class="text-primary" id="view_row"> <i class="far fa-eye"></i></a></div></td>
                    </tr>
                `;

                $("#tableData tbody").append(rowHtml);
            });
        },

        error: function (request, error) {
            console.error(error);
        }
    });
}

getData();


function getRowsUpdate() {
  $("#tableData tr").click(function() {
      var currentRow = $(this).closest("tr");
      var lclID = currentRow.find("td:eq(1)").text();
      var lclName = currentRow.find("td:eq(2)").text();
      
      $("#txtName1").val(lclName);
      $("#edit_id").val(lclID);

  });
}

$(document).on("click", "#view_row", function () {
  const $tr = $(this).closest("tr");
  let lclID = $tr.data("bk-id");
  if (!lclID) lclID = $tr.find("td:eq(1)").text().trim();

  $("#view_id").val(lclID);

  $.ajax({
    url: `/booking_details/${encodeURIComponent(lclID)}/`,
    type: "GET",
    dataType: "json",
    success: function (resp) {
      const b = resp.booking || {};
      const ph = resp.predict_history || {};
      const d = resp.design || {};
      const steps = resp.steps || [];

      let deImg = "";
      if (d.de_image) deImg = d.de_image.substring(3);

      $("#view_title").text(`${d.de_name || b.de_name || "Design"}`);

      const bookingBlock = `
        <div class="card mb-3">
          <div class="card-header"><strong>Booking</strong></div>
          <div class="card-body">
            <div class="row">
              <div class="col-sm-6"><div><strong>Status:</strong> ${b.status ?? ""}</div></div>
              <div class="col-sm-6"><div><strong>User:</strong> ${b.user_email ?? ""}</div></div>
              <div class="col-sm-12"><div><strong>Booked On:</strong> ${b.booking_date ?? ""} ${b.booking_time ?? ""}</div></div>
              <div class="col-sm-12"><div><strong>Design:</strong> ${b.de_name ?? ""}</div></div>
            </div>
          </div>
        </div>
      `;

      const phBlock = `
        <div class="card mb-3">
          <div class="card-header"><strong>User Summary</strong></div>
          <div class="card-body">
            <div class="row">
              <div class="col-sm-3"><div><strong>Age:</strong> ${ph.ph_age ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Gender:</strong> ${ph.ph_gender ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Occasion:</strong> ${ph.ph_occasion ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Height (cm):</strong> ${ph.ph_height_cm ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Chest (cm):</strong> ${ph.ph_chest_cm ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Waist (cm):</strong> ${ph.ph_waist_cm ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Hips (cm):</strong> ${ph.ph_hips_cm ?? ""}</div></div>
              <div class="col-sm-3"><div><strong>Shoulder (cm):</strong> ${ph.ph_shoulder_cm ?? ""}</div></div>
              <div class="col-sm-6"><div><strong>Recommended Outfit:</strong> ${ph.ph_predicted_outfit ?? ""}</div></div>
              <div class="col-sm-6"><div><strong>Predicted By:</strong> ${ph.ph_created_by ?? ""}</div></div>
            </div>
          </div>
        </div>
      `;

      const designBlock = `
        <div class="card mb-3">
          <div class="card-header"><strong>Design</strong></div>
          <div class="card-body">
            <div class="row align-items-start">
              <div class="col-md-6 mb-3">
                <div class="h5 mb-1">${d.de_name || b.de_name || "-"}</div>
                <span class="badge badge-${(d.de_status || "0")==="0" ? "secondary" : "info"}">
                  ${(d.de_status || "0")==="0" ? "Active" : "Active"}
                </span>
              </div>
              <div class="col-md-6">
                ${deImg ? `<img src="${deImg}" style="width:200px; height:200px; object-fit:cover;" class="rounded" alt="Design Image">` : `<div class="text-muted">No image</div>`}
              </div>
            </div>
          </div>
        </div>
      `;

      const stepsCards = steps.map((s) => {
        const imgPath = s.ar_image ? s.ar_image.substring(3) : "";
        return `
          <div class="card mb-3">
            <div class="card-body">
              <div class="h6 mb-2">${s.ar_name || ""}</div>
              ${imgPath ? `<img src="${imgPath}" style="width:200px; height:200px; object-fit:cover;" class="rounded mb-2" alt="${s.ar_name || ""}">` : ``}
              <div class="text-muted">${s.ar_description || ""}</div>
              <div class="mt-2">
                <span class="badge badge-${(s.ar_status || "0")==="0" ? "secondary" : "success"}">
                  ${(s.ar_status || "0")==="0" ? "Active" : "Active"}
                </span>
              </div>
            </div>
          </div>
        `;
      }).join("");

      const stepsBlock = `
        <div class="card">
          <div class="card-header"><strong>Design Steps</strong></div>
          <div class="card-body">
            ${stepsCards || `<div class="text-muted">No steps available.</div>`}
          </div>
        </div>
      `;

      $("#view_body").html(bookingBlock + phBlock + designBlock + stepsBlock);
    },
    error: function (xhr) {
      $("#view_title").text("Booking Details");
      $("#view_body").html(`<div class="alert alert-danger">Failed to load booking details.</div>`);
      console.error(xhr.responseText || xhr.statusText);
    }
  });
});



$(document).on("click", "#btn_update", function () {

    if ($("#selStatus").val().trim().length < 1) {
      snackbar_error("Please Select Role");
      $("#selStatus").focus();
      return false;
    }
    
    var formData = new FormData();
    formData.append("selStatus", $("#selStatus").val());
    formData.append("id", $("#edit_id").val());
    formData.append("action", "update");
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

    $.ajax({
      beforeSend: function () {
        $(".btn .spinner-border").show();
        $("#btn_update").attr("disabled", true);
      },
      url: "/update_status/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (result) {
        snackbar_success("Details Updated Succesfully");
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