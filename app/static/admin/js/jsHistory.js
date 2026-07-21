function getData() {
  const formData = new FormData();
  formData.append("action", "getData");
  formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

  $.ajax({
    url: "/admin_history_details/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      $("#tableData tbody").empty();

      if (!Array.isArray(response) || response.length === 0) {
        $("#tableData tbody").append(`<tr><td colspan="13" class="text-center text-muted">No records</td></tr>`);
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

        $("#tableData tbody").append(rowHtml);
      });
    },
    error: function (request, error) {
      console.error(error);
      $("#tableData tbody").html(`<tr><td colspan="13" class="text-center text-danger">Failed to load</td></tr>`);
    }
  });
}

getData();
