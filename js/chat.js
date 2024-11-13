$(document).ready(function() {
    $('#form_msg_input').submit(function(event) {

        event.preventDefault(); // Prevent form submission

        // Message to append
        var message = '<div class="chat_bubble_bot"> <p class="role_style">You</p> <p class="message_style">' + $('#input_msg_text').val() + '</p></div>';

        // value
        var value = $('#input_msg_text').val();

        // Append message to chat
        $('#chat_msg_id').append(message);
        
        // Clear input field
        $('#input_msg_text').val('');

        // Scroll to bottom
        $('#chat_conv_id').scrollTop($('#chat_conv_id')[0].scrollHeight);

        // Send message to server
        $.ajax({
            url: '/api/v1/SmartHelp/llm/chat',
            type: 'post',
            contentType: 'application/json',  // Specify the content type
            data: JSON.stringify({            // Convert the data to JSON format
                query: value
            }),
            success: function(response) {

                // Append response to chat
                var message_bot = '<div class="chat_bubble_bot"><p class="role_style">Assistant</p> <p class="message_style">' + response["response"] + '</p></div>';

                // Append message to chat
                $('#chat_msg_id').append(message_bot);

                // Scroll to bottom
                $('#chat_conv_id').scrollTop($('#chat_conv_id')[0].scrollHeight);
            },
            error: function(error) {
                console.log(error);
            }
        });

    });
});