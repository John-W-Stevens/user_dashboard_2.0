// #edit_profile_form -> form for editing user profile

// input fields:

// #first_name
// #last_name
// #email
// #new_password
// #new_password_confirm
// #city
// #state
// #country
// #auth_password

// CALLBACK FUNCTIONS

function validate_email_format(email){
    /// Returns true if email is valid, false otherwise ///
    var re = /^\w+([-+.'][^\s]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    return re.test(email)
}
function get_profile_id(){
    return $("#profile.id").val()
}


$("#edit_profile_form_button").on("click",function(e){
    e.preventDefault()
    console.log("Form stopped")
    // check first_name, last_name, passwords
    errors = 0
    if ($("#first_name").val() == ""){
        // error -> first name cannot be blank
        $("#first_name_label").html('                                <label>First Name</label>&nbsp<small class="error_message">First name cannot be blank</small>')
        errors += 1
    }
    if ($("#last_name").val() == ""){
        // error -> last name cannot be blank
        $("#last_name_label").html('                                <label>Last Name</label>&nbsp<small class="error_message">Last name cannot be blank</small>')
        errors += 1
    }
    if ($("#new_password").val() != ""){
        if ($("#new_password").val().length < 8){
            $("#new_password_label").html('                                <label>New Password</label>&nbsp<small class="error_message">Passwords must have at least 8 characters</small>')
            errors += 1
        }
    }
    if ($("#new_password").val() != $("#new_password_confirm").val()){
        // error -> passwords must match
        $("#new_password_confirm_label").html('                                <label>New Password</label>&nbsp<small class="error_message">Passwords must match</small>')
        errors += 1
    }
    if ($("#email").val() == ""){
        // error -> email cannot be blank
        $("#email_label").html('                                <label>Email Address</label>&nbsp<small class="error_message">Email cannot be blank</small>')
        errors += 1
    }
    else if (!validate_email_format($("#email").val())){
        // error -> invalid email
        $("#email_label").html('                                <label>Email Address</label>&nbsp<small class="error_message">Invalid Email address</small>')
        errors += 1
    }
    // check if email is already used
    if ($("#auth_password").val() == ""){
        $("#auth_password_label").html('                          <label>Verify current password:</label>&nbsp<small class="error_message">Required</small>')
        errors += 1
    }

    console.log("The number of errors is", errors)
    if (errors > 0){
        console.log("Hello!")
        return
    }
    else if (errors == 0) {
    // submit form
        $("#edit_profile_form").submit()
        console.log("Form submitted.")
    }
     
})