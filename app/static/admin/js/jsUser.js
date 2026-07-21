
function getData() {

    const formData = new FormData();
    formData.append("action", "getData");
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

    $.ajax({

        url: "/admin_user_details/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
        $("#tableData tr:gt(0)").remove();
        for(var i = 0; i < response.length; i++) {
            var j = i + 1;
            $("#tableData").append('<tr><td>'+j+'</td><td style="display: none;">'+response[i].rg_id+'</td><td>'+response[i].rg_name+'</td><td>'+response[i].rg_email+'</td><td>'+response[i].rg_mobile+'</td><td><div class="d-flex" style="justify-content: space-evenly;"><a href="javascript:void(0);" id="edit_row" title="View/Edit" data-toggle="modal" data-target="#edit_modal" class="text-primary" onClick="getRowsUpdate();"> <i class="fas fa-eye"></i></a></div></td></tr>');
        }
        },
        error: function (request, error) {
            console.error(error);
        },
        complete: function () {

        },
    });

}

function formatDate(dateStr) {
    const [year, month, day] = dateStr.split("-");
    return `${day}-${month}-${year}`;
}
getData();

function getRowsUpdate() {
  $("#tableData tr").click(function() {
      var currentRow = $(this).closest("tr");
      var lclEmail = currentRow.find("td:eq(3)").text();
      $("#edit_id").val(lclEmail);
      getHistoryData()
  });
}

function getHistoryData() {
  const formData = new FormData();
  formData.append("action", "getData");
  formData.append("email", $("#edit_id").val());
  formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

  $.ajax({
    url: "/admin_history_details_individual/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      $("#tableData1 tbody").empty();

      if (!Array.isArray(response) || response.length === 0) {
        $("#tableData1 tbody").append(
          `<tr><td colspan="13" class="text-center text-muted">No records</td></tr>`
        );
        return;
      }

      response.forEach(function (item, index) {
        const slNo = index + 1;

        const createdDate = item.ph_created_date ? new Date(item.ph_created_date) : null;
        const formattedDate = createdDate
          ? createdDate.toLocaleString("en-IN", {
              day: "2-digit",
              month: "2-digit",
              year: "numeric",
              hour: "numeric",
              minute: "2-digit",
              hour12: true,
            })
          : "-";

        const rowHtml = `
          <tr>
            <td>${slNo}</td>
            <td style="display:none;">${item.ph_id ?? ""}</td>
            <td>${item.ph_created_by ?? ""}</td>
            <td>${item.ph_age ?? ""}</td>
            <td>${item.ph_gender ?? ""}</td>
            <td>${item.ph_height_cm ?? ""}</td>
            <td>${item.ph_chest_cm ?? ""}</td>
            <td>${item.ph_waist_cm ?? ""}</td>
            <td>${item.ph_hips_cm ?? ""}</td>
            <td>${item.ph_shoulder_cm ?? ""}</td>
            <td>${item.ph_occasion ?? ""}</td>
            <td>${item.ph_predicted_outfit ?? ""}</td>
            <td>${formattedDate}</td>
          </tr>
        `;

        $("#tableData1 tbody").append(rowHtml);
      });
    },
    error: function (request, error) {
      console.error(error);
      $("#tableData1 tbody").html(
        `<tr><td colspan="13" class="text-center text-danger">Failed to load</td></tr>`
      );
    },
  });
}

getHistoryData();