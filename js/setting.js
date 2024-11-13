function modify_prompt() {

    var data = {
        "prompt" : document.getElementById("prompt_input").value
    };

    $.ajax({
        url: '/api/v1/SmartHelp/user/llm/modify',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {

            window.location.replace("/LLM/setting");
        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });
}

function modify_llm_configuration() {

    var data = {
        "context_length" : document.getElementById("context_length").value,
        "max_length" : document.getElementById("max_new_tokens").value,
        "gpu_layers" : document.getElementById("gpu_layers").value
    };

    $.ajax({
        url: '/api/v1/SmartHelp/user/llm/configuration/modify',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {

        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });
}

function modify_splitter_configuration () {
    
        var data = {
            "chunk_size" : document.getElementById("chunk_size").value,
            "chunk_overlap" : document.getElementById("chunk_overlap").value,
            "separator" : document.getElementById("separator").value
        };
    
        console.log(data);

        $.ajax({
            url: '/api/v1/SmartHelp/user/splitter/modify',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: (response) => {
    
            },
            error: (error) => {
                console.error('POST request failed:', error);
            }
        });
    }

function modify_credentials() {

    var data = {
        "email" : document.getElementById("email_label").innerText,
        "name" : document.getElementById("pseudo_label").innerText
    };

    $.ajax({
        url: '/api/v1/SmartHelp/user/credentials/modify',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {
            window.location.replace("/setting");
        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });
}

function modify_password() {
    
        var data = {
            "pwd" : document.getElementById("user_pwd").value
        };
    
        $.ajax({
            url: '/api/v1/SmartHelp/user/password/modify',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: (response) => {
    
                window.location.replace("/setting");
            },
            error: (error) => {
                console.error('POST request failed:', error);
            }
        });
    }

function change_name_ui () {

    var name = document.getElementById("pseudo_label");
    var new_name = document.getElementById("user_name").value;

    // Delete innerText
    name.innerText = new_name;

    // Close modal
    $('#modal_name').modal('hide');
}

function change_email_ui () {

    var name = document.getElementById("email_label");
    var new_email = document.getElementById("user_email").value;

    // Delete innerText
    name.innerText = new_email;

    // Close modal
    $('#modal_email').modal('hide');
}