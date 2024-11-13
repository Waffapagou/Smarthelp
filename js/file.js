function delete_file(element) {

    var data = {
        "file_name" : element["file_name"]
    };

    $.ajax({
        url: '/api/v1/SmartHelp/file/delete',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {
            console.log(response);
            window.location.replace("/file");
        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });

}

function download_file(element) {

    $.ajax({
        url: '/api/v1/SmartHelp/file/download/'+element["file_id"],
        type: 'GET',
        success: (response) => {},
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });

}