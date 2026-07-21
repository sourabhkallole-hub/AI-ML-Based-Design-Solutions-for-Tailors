
function getData() {

    const formData = new FormData();
    formData.append("action", "getData");
    formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

    $.ajax({

        url: "/admin_contact_details/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
        $("#tableData tr:gt(0)").remove();
        for(var i = 0; i < response.length; i++) {
            var j = i + 1;
            $("#tableData").append('<tr><td>'+j+'</td><td style="display: none;">'+response[i].co_id+'</td><td>'+response[i].co_name+'</td><td>'+response[i].co_email+'</td><td>'+response[i].co_mobile+'</td><td>'+response[i].co_subject+'</td><td>'+response[i].co_message+'</td></tr>');
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