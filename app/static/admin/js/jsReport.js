
function getData() {

  var formData = new FormData();
  formData.append("action", "getData");
  formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());
  
  $.ajax({
  
      url: "/admin_report_details/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
          const ctx = document.getElementById('expenseChart').getContext('2d');
          
          const categories = response.categories;
          const amounts = response.amounts;
      
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: categories,
              datasets: [{
                label: 'Expenses (₹)',
                data: amounts,
                backgroundColor: [
                  '#4e79a7',
                  '#f28e2b',
                  '#e15759',
                  '#76b7b2',
                  '#59a14f'
                ],
                borderColor: '#333',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: 'Amount (₹)'
                  }
                },
                x: {
                  title: {
                    display: true,
                    text: 'Category'
                  }
                }
              },
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                },
                title: {
                  display: true,
                  text: 'Expense Breakdown by Category'
                }
              }
            }
          });
      },
      error: function (request, error) {
        console.error(error);
      },
      complete: function () {
  
      },
    });
  
  }

  getData();