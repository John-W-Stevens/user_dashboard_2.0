// input validation for new messages and comments

$("#message_submit_button").on("click", function(e){
    e.preventDefault()
    if ($("#message_textarea").val() == ""){
        // empty string
        $("#message_error").text("Cannot post empty message")
    }
    else {
        $("#message_submit_form").submit()
    }
})

var message_id;

// input validation for new comment
$(".comment_submit_button").on("click", function(e){
    e.preventDefault()
    message_id = $(this).attr("data-message-id")
    var textarea = $(`#comment_${message_id}`)
    if ($(`#comment_${message_id}`).val() == ""){
        $(`#comment_label_${message_id}`).text("Cannot submit empty comment")
    }
    else {
        $(`#comment_submit_form_${message_id}`).submit()
    }
    
})
// ajax handles new comment form submisson
$(".comment_submit_form").submit(function(e){
    e.preventDefault()
    $.ajax({
        url: `/user/${profile_id}`,
        method: 'post',
        data: $(this).serialize(),
        success: function(serverResponse){
          $(`#${message_id}_comments_container`).html(serverResponse) // replace the contents of the comments div with the serverResponse
          $("#edit_comment_modal").modal('hide')
          $(`#comment_${message_id}`).val("")
        }
      })
})

// edit a comment
// populate edit comment modal
var message_id;
var comment_id;
var comment_content;
var profile_id = $("#container").attr("data-profile-id")

// $(".edit_comment_link").on("click", function(){
$(document).on("click",".edit_comment_link",function(){
    message_id = $(this).attr("data-message-id")
    comment_id = $(this).attr("data-comment-id")
    comment_content = $(this).attr("data-comment")

    $("#edit_comment_message_id").val(message_id) // set hidden input to include message.id
    $("#edit_comment_comment_id").val(comment_id) // set hidden input to include comment.id
    $("#comment_to_edit").text(comment_content)
    $("#comment_to_edit").val(comment_content)
})

$("#comment_edit_form").on("submit",function(e){
    e.preventDefault()
    // input validation
    if ($("#comment_to_edit").val() == ""){
        $("#edit_comment_header").html('              <h3 class="modal-title" id="editComment" style="display: inline-block">Edit Comment:</h3>&nbsp&nbsp&nbsp<small style="color: red; display: inline-block">Cannot submit empty comment</small>')
        $("#comment_to_edit").val(comment_content)
    }
    else {
        // ajax handles comment edits
        $.ajax({
            url: `/user/${profile_id}`,
            method: 'post',
            data: $(this).serialize(),
            success: function(serverResponse){
              $(`#${message_id}_comments_container`).html(serverResponse) // replace the contents of the comments div with the serverResponse
              $("#edit_comment_modal").modal('hide')
            }
        })  
    }
})

// Delete a comment with AJAX
$(document).on("click",".delete_comment_link",function(){
    message_id = $(this).attr("data-message-id")
    comment_id = $(this).attr("data-comment-id")
    $("#delete_comment_message_id").val(message_id) // set hidden input to include message.id
    $("#delete_comment_comment_id").val(comment_id) // set hidden input to include comment.id
})

$("#comment_deletion_form").on("submit",function(e){
    e.preventDefault()
    $.ajax({
        url: `/user/${profile_id}`,
        method: 'post',
        data: $(this).serialize(),
        success: function(serverResponse){
          $(`#${message_id}_comments_container`).html(serverResponse) // replace the contents of the comments div with the serverResponse
          $("#delete_comment_modal").modal('hide')
        }
    })
})