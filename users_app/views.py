from django.shortcuts import render, redirect
from . import models
import bcrypt

##### DEVELOPMENT ######
def display_post(request):
    print("..........................")
    print("Printing data from request.POST.......")
    for k,v in request.POST.items():
        print(f"Key: {k}, Value: {v}")
    print("..........................")
    print("Printing data from request.FILES.......")
    if request.FILES == {}:
        print("No files uploaded")
    else:
        for k,v in request.FILES.items():
            print(f"Key: {k}, Value: {v}")
    print("..........................")

##### DEVELOPMENT ######


####### Helper Functions ########

def logged_user(request):    
    """ Get logged-in User object """
    return models.User.objects.filter(id=request.session["user_id"])[0]

def is_admin(request):
    """ Returns True if logged-in user is an admin, False otherwise """
    if request.session["user_id"] == None:
        return False
    return logged_user(request).level == 9

def initialize_session(request):
    try:
        request.session["user_id"]
        # handles the rare case where an administrator deletes their own account
        if not models.User.objects.filter(id=request.session["user_id"]):
            request.session["user_id"] = None
    except KeyError:
        request.session["user_id"] = None

def get_context(request, index=False, users=False):
    if index:
        if request.session["user_id"] == None:
            context = {}
        else:    
            context = {"user": logged_user(request),}
        return context
    if users:
        context = {
            "user": logged_user(request),
            "users": models.User.objects.all(),
        }
        return context
    else:
        try:
            errors = request.session["errors"]
        except KeyError:
            errors = None

        if request.session["user_id"] == None:
            context = {"user": "none","errors": errors,}
        else:
            context = {"user": logged_user(request),"errors": errors,}
        return context

####### Helper Functions ########

# Login and Registration Functions:

def index(request):
    """
    GET -> gets home page
    """
    initialize_session(request)
    context = get_context(request, index=True)    
    return render(request, "index.html", context)
# GET -> get home page

def login(request):
    """
    GET -> gets login page 
    POST -> authenticates login attempt
    """
    
    if request.POST:
        # authenticate user credentials from anywhere on the site:
        try:
            request.POST["auth"]
            errors = models.User.objects.login_validations(request.POST)
            if len(errors) == 0:
                return redirect(request.POST["auth"])
            else:
                return redirect(request.POST["origin"])
        except KeyError:
            pass

        # login attempt made from login page:
        errors = models.User.objects.login_validations(request.POST)
        if len(errors) > 0:
            request.session["errors"] = errors    
            return redirect("/login")
        else:
            request.session["user_id"] = models.User.objects.filter(email=request.POST["email"])[0].id
            return redirect("/")

    else: # request.GET
        context = get_context(request)    
        request.session["errors"] = None # Reset errors
        return render(request, "login.html", context)
# GET -> gets login page 
# POST -> authenticates login attempt

def registration(request):
    """
    GET -> gets registration page
    POST -> authenticates registration attempt
    """
    if request.POST:
        errors = models.User.objects.registration_validations(request.POST)
        if len(errors) > 0:
            request.session["errors"] = errors
            return redirect("/registration")
        else:
            # create new user
            new_user = models.User.objects.create(
                first_name = request.POST["first_name"],
                last_name = request.POST["last_name"],
                email = request.POST["email"],
                password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            )
            
            if len(models.User.objects.all()) == 1:
                new_user.level = 9 # make the first user to register an administrator    
            else:
                try:
                    request.POST["admin"]
                    new_user.level = 9
                except KeyError:
                    new_user.level = 1

            new_user.save()
            
            if is_admin(request):
                return redirect("/users")

            return redirect("/login")
    
    else: # request.GET
        # restrict access to this url for users that are already logged-in, unless they are administrators
        if request.session["user_id"] == None:
            context = get_context(request)
            request.session["errors"] = None # Reset errors
            return render(request, "registration.html", context)
        
        elif logged_user(request).level != 9:
            return redirect("/")

        else:
            context = get_context(request)
            request.session["errors"] = None # Reset errors
            return render(request, "registration.html", context)
# GET -> gets registration page
# POST -> authenticates registration attempt                

def logout(request):
    del request.session["user_id"]
    return redirect("/")
# POST -> destroys session

# Users Functions
def users(request):
    context = get_context(request, users=True)
    return render(request, "users.html", context)

def user(request, profile_id):
    """
    GET -> displays the user profile page
    POST -> handles profile edits, deletions, messages, and comments
    """
    if request.POST:
        display_post(request)
        ########### Post Message ##########
        try:
            request.POST["new_message"]
            profile = models.User.objects.filter(id=profile_id)[0]
            new_message = models.Message.objects.create(content=request.POST["message"], recipient=profile, author=logged_user(request))
            new_message.save()
            return redirect(f"/user/{profile_id}")
        
        except KeyError:
            pass

        ########### Post Comment ###########
        try:
            request.POST["new_comment"]
            profile = models.User.objects.filter(id=profile_id)[0]
            print("Got profile")
            message = models.Message.objects.filter(id= int(request.POST["message_id"]))[0]
            print("Got message")
            new_comment = models.Comment.objects.create(content=request.POST["comment"], author=logged_user(request),message=message )
            new_comment.save()
            context = {
                "user": logged_user(request),
                "message": models.Message.objects.filter(id=int(request.POST["message_id"]))[0]
            }
            return render(request, "comments.html", context)
            # return redirect(f"/user/{profile.id}")

        except KeyError:
            pass

        ########### Edit Comment #############
        try:
            request.POST["edit_comment"]
            print("We are making an edit to a comment")

            # handle ajax request to update comments
            comment = models.Comment.objects.filter(id=int(request.POST["comment_id"]))[0]
            comment.content = request.POST["edited_comment"]
            comment.save()

            context = {
                "user": logged_user(request),
                "message": models.Message.objects.filter(id=int(request.POST["message_id"]))[0]
            }
            return render(request, "comments.html", context)
        except KeyError:
            pass

        ########### Delete Comment #############
        try:
            request.POST["delete_comment"]
            print("We are deleting a comment")

            comment = models.Comment.objects.filter(id=int(request.POST["comment_id"]))[0]
            comment.delete()
            context = {
                "user": logged_user(request),
                "message": models.Message.objects.filter(id=int(request.POST["message_id"]))[0]
            }
            return render(request, "comments.html", context)
        except KeyError:
            pass

        ###### a. Handle Edit to Profile ######

        ########### Authenticate Credentials ###########
        user = {
            "email": logged_user(request).email,
            "password": request.POST["current_password"]
        }
        errors = models.User.objects.login_validations(user)
        if len(errors) > 0:
            print("Incorrect password rerouting to user profile page")
            # user entered the wrong password
            try:
                request.POST["destroy"]
                return redirect("/users")
            except KeyError:
                return redirect(f"/user/{profile_id}")
        ########### Authenticate Credentials ###########

        ############# Account Deletion ###############
        try:
            request.POST["destroy"]
            print("Deleting account....")
            profile = models.User.objects.filter(id=profile_id)[0]
            if user == profile:
                # the user is deleting their own account
                profile.delete()
                return redirect("/")
            else:
                profile.delete()
                return redirect("/users")
        except KeyError:
            pass
        ############# Account Deletion ###############

        ############# Input Validation for Account Edit #############
        errors = models.User.objects.update_profile_validations(request.POST, profile_id)
        if len(errors) > 0:
            print("Invalid input, rerouting to user profile page")
            # user entered an invalid email address
            return redirect(f"/user/{profile_id}")
        ############# Input Validation for Account Edit #############

        ############# Account Update ##############
        # update profile
        print("Updating profile....")
        profile = models.User.objects.filter(id=profile_id)[0]
        profile.first_name = request.POST["first_name"]
        profile.last_name = request.POST["last_name"]
        profile.email = request.POST["email"]
        
        if request.POST["password"] != "":
            profile.password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        
        if logged_user(request) != profile:
            if request.POST["user_level"] == "Admin":
                profile.level = 9
            else:
                profile.level = 1
        if request.POST["city"] != profile.city:
            profile.city = request.POST["city"]
        if request.POST["state"] != profile.state:
            profile.state = request.POST["state"]
        if request.POST["country"] != profile.country:
            profile.country = request.POST["country"]
        if request.FILES != {}:
            # delete the old profile image
            profile.profile_photo.delete()
            # change the user's profile image
            profile.profile_photo = request.FILES["profile_image_upload"]
        profile.description = request.POST["description"]
        profile.save()
        return redirect(f"/user/{profile_id}")
        ############# Account Update ##############



    # GET request
    else:
        profile = models.User.objects.filter(id=profile_id)[0]
        context = {
            "user": logged_user(request),
            "profile": profile,
            "messages": profile.messages_received.all().order_by("-created_at"),
        }
        return render(request,"user.html", context)

