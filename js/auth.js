/**
 * Sends a POST request to the API.
 * 
 */
function register() {

    // verify that the fields are not empty
    if (document.getElementById("signup-name").value === "" || document.getElementById("signup-email").value === "" || document.getElementById("signup-password").value === "" || document.getElementById("signup-role").value === "") {
        return;
    }

    // verify that the email is valid
    var email = document.getElementById("signup-email").value;
    if (!email.includes("@")) {
        return;
    }

    // verify that both passwords match
    var password = document.getElementById("signup-password").value;
    var confirmPassword = document.getElementById("signup-password-verify").value;

    if (password !== confirmPassword) {
        return;
    }

    var data = {
        "name" : document.getElementById("signup-name").value,
        "email" : document.getElementById("signup-email").value,
        "pwd" : document.getElementById("signup-password").value,
        "type" : document.getElementById("signup-role").value
    };

    $.ajax({
        url: '/api/v1/SmartHelp/user/create',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {
            // Send get request to activate account
            $.ajax({
                url: '/api/v1/SmartHelp/account/activate/'+ response,
                type: 'GET',
                success: (response_3) => {

                    // Send the request to create the LLM prompt
                    var llm_data = {
                        "user_token" : response,
                        "prompt" : "En utilisant uniquement le contexte suivant : {context}. Répond à la question suivante en Français avec une réponse courte : {query}.",
                        "llm" : {
                            "name" : "mistral"
                        }
                    };

                    $.ajax({
                        url: '/api/v1/SmartHelp/user/llm/create',
                        type: 'POST',
                        data: JSON.stringify(llm_data),
                        contentType: 'application/json',
                        success: (response_2) => {
                            // create user session
                            $.ajax({
                                url: '/api/v1/SmartHelp/user/session/create/'+response,
                                type: 'GET',
                                success: (response_2) => {
                                    window.location.replace("/");
                                },
                                error: (error) => {
                                    console.error('GET request failed:', error);
                                }
                            });
                        },
                        error: (error) => {
                            console.error('GET request failed:', error);
                        }
                    });
                    
                },
                error: (error) => {
                    console.error('GET request failed:', error);
                }
            });
        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });
}

/**
 * Logs in the user by sending a POST request to the server with the provided email and password.
 * If the login is successful, a session is created and the user is redirected to the home page.
 */
function login() {
    var data = {
        "email" : document.getElementById("signin-email").value,
        "pwd" : document.getElementById("signin-password").value
    };

    $.ajax({
        url: '/api/v1/SmartHelp/user/login',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {
            // Send get request to create session
            $.ajax({
                url: '/api/v1/SmartHelp/user/session/create/'+response,
                type: 'GET',
                success: (response_2) => {
                    window.location.replace("/");
                },
                error: (error) => {
                    console.error('GET request failed:', error);
                }
            });
        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });
}

// Function to destroy session
function destroy_session() {

    $.ajax({
        url: '/api/v1/SmartHelp/user/session/destroy',
        type: 'get',
        success: (response) => {
            // Go to login page
            window.location.replace("/login");
        },
        error: (error) => {
            console.error('POST request failed:', error);
        }
    });
}