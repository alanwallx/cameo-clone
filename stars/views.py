from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from .models import Star, User, Order, Video
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

# Create your views here.


class OrderForm(forms.Form):
    recipient = forms.CharField(label="To", max_length=32)
    messagefrom = forms.CharField(label="From", max_length=32)
    custommessage = forms.CharField(widget=forms.Textarea, label="Custom Message", max_length=500)
    username = forms.CharField(widget=forms.HiddenInput(), required=True)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["name", "videofile"]
        widgets = {"name": forms.HiddenInput()}


class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = ["firstname", "lastname", "price", "occupation",
                  "username", "cover", "application_letter"]
        labels = {
            'firstname': _('First Name'),
            'lastname': _('Last Name'),
            'cover': _('Photo'),
            'application_letter': _('Application Details'),
            'reason_for_status_change': _('Reason for status change')
        }
        help_texts = {
            'price': _('The price you would like to charge per video'),
            'username': _('Pick a unique username to become the URL for your star profile'),
            'cover': _('Upload a friendly photo of your face'),
            'application_letter': _('Please let us know why you should be considered, include your social media profiles, how many followers you have, and any information to help us approve your star profile.')
        }


class StarAdmin(forms.ModelForm):
    class Meta:
        model = Star
        fields = ["firstname", "lastname", "price", "occupation",
                  "username", "cover", "application_letter", "status", "reason_for_status_change"]
        labels = {
            'firstname': _('First Name'),
            'lastname': _('Last Name'),
            'cover': _('Photo'),
            'application_letter': _('Application Details'),
            'reason_for_status_change': _('Reason for status change')
        }

# HOME PAGE:


def stars(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = "Not Logged In"
    context = {
        "stars": Star.objects.filter(status="APPROVED"),
        "user": user
    }
    return render(request, "stars/index.html", context)


def star(request, username):
    try:
        star_id = Star.objects.get(username=username)
    except Star.DoesNotExist:
        raise Http404("Star does not exist")
    if request.user.is_authenticated:
        customer = request.user.username
    else:
        customer = ""
    form = OrderForm(initial={'messagefrom': customer, 'username': username})
    context = {
        "star": star_id,
        "form": form,
        "customer": customer
    }
    return render(request, "stars/starpage.html", context)


def profile(request, pk):
    try:
        star_id = Star.objects.get(pk=pk)
    except Star.DoesNotExist:
        raise Http404("Star does not exist")
    context = {
        "star": pk,
    }
    return render(request, "stars/profile.html", context)


def order(request):
    if request.method == "GET":
        return HttpResponse("Direct Access Prohibited")
    # POST:
    form = OrderForm(request.POST)
    # Check if form data is valid (server-side)
    if form.is_valid():
        recipient = form.cleaned_data["recipient"]
        messagefrom = form.cleaned_data["messagefrom"]
        custommessage = form.cleaned_data["custommessage"]
        username = form.cleaned_data["username"]
        customer = request.user
        star = Star.objects.get(username=username)
        # star = Star.objects.get(pk=1)
        # username = star.username
        price = star.price
        placed = True
        order_instance = Order.objects.create(customer=customer, recipient=recipient, messagefrom=messagefrom,
                                              custommessage=custommessage, starbooked=star, price=price)
        # get the order id:
        order_id = str(Order.objects.last().id)
        # TODO check the order_id refers to the current order
        # prepare the email for the star:
        emailsubject = "A video request from Instarvid. Ref[" + order_id + "]"
        emailmessage = "You have a request for a video from a user of Instarvid! They say: " + \
            custommessage + " From: " + messagefrom + ". To: " + recipient + \
            ". Please visit http://127.0.0.1:8000/stars/upload/" + order_id + " to upload your recorded video."
        emailfrom = 'orders@instarvid.com'
        # emailto = star.email
        emailto = star.owner.email
        send_mail(emailsubject, emailmessage, emailfrom, [emailto], fail_silently=False,)
        # return HttpResponse("Order submitted")
        context = {
            "star": star,
            "form": "Thank you!",
            "submitted": True,
            "order_id": order_id
        }
        return render(request, "stars/starpage.html", context)


def starcreate(request):
    if request.method == "GET":
        form = StarForm()
        context = {
            "form": form,
        }
        return render(request, "stars/create.html", context)
    else:  # POST
        form = StarForm(request.POST, request.FILES)
        if form.is_valid():
            newstar = form.save(commit=False)
            newstar.status = 'PENDING'
            newstar.owner = request.user
            # todo: make sure username is unique, add number to it maybe? and remove "unique" attribute in the model
            if Star.objects.filter(username=newstar.username).exists():
                context = {
                    "form": form,
                    "warning": "Username already exists"
                }
                return render(request, "stars/create.html", context)
            newstar.save()
            context = {
                "success": "Thank you. Our staff will evaluate your application and get back to you within 5 days.",
            }
            return render(request, "stars/create.html", context)
        else:
            context = {
                "warning": form.errors,
            }
            return render(request, "stars/create.html", context)

# this is for owners to edit a star profile:


def staredit(request, pk):
    instance = get_object_or_404(Star, pk=pk)
    form = StarForm(request.POST or None, instance=instance)
    if request.method == "GET":
        # check if this user is the owner of the star profile or an admin:
        if (instance.owner.id != request.user.id) and not (request.user.is_superuser):
            return HttpResponse("You can only change profiles of stars you own.")
        context = {
            "star": Star.objects.get(pk=pk),
            "form": form,
            "message": "",
            "reason_for_status_change": instance.reason_for_status_change,
            "status": instance.status,
        }
        return render(request, "stars/edit.html", context)
    else:  # POST

        if form.is_valid():
            editedstar = form.save(commit=False)
            # logic for status after user changes:
            if editedstar.status == 'PENDING':
                editedstar.status = 'PENDING'
            elif editedstar.status == 'RETURNED':
                editedstar.status = 'RESUBMITTED'
            elif editedstar.status == 'RESUBMITTED':
                editedstar.status = 'RESUBMITTED'
            elif editedstar.status == 'APPROVED':
                editedstar.status = 'APPROVED'
            elif editedstar.status == 'SUSPENDED':
                editedstar.status = 'RESUB_SUSPENDED'
            elif editedstar.status == 'RESUB_SUSPENDED':
                editedstar.status = 'RESUB_SUSPENDED'
            elif editedstar.status == 'DECLINED':
                editedstar.status = 'RESUB_DECLINED'
            elif editedstar.status == 'RESUB_DECLINED':
                editedstar.status = 'RESUB_DECLINED'
            else:
                return HttpResponse("There is an error in the status choices, the status is not in the list of allowed status")
            editedstar.save()
            context = {
                "message": "We have received your changes stareditform",
                "pk": pk,
                "star": Star.objects.get(pk=pk)
            }
        else:
            context = {
                "message": form.errors,
                "pk": pk,
            }
        return render(request, "stars/profile.html", context)

# this is for administrators to change the status of an order and the owner gets emailed:


def staradmin(request, pk):
    instance = get_object_or_404(Star, pk=pk)
    form = StarAdmin(request.POST or None, instance=instance)
    if request.method == "GET":
        # check if this user is the owner of the star profile:
        if not (request.user.is_superuser):
            return HttpResponse("Only administrators can change the status of a star profile.")
        context = {
            "form": form,
            "message": "",
            "reason_for_status_change": instance.reason_for_status_change,
            "status": instance.status,
            "star": Star.objects.get(pk=pk)
        }
        return render(request, "stars/staradmin.html", context)
    else:  # POST
        if form.is_valid():
            # prepare the email for the owner:
            emailsubject = "The status of your star profile has changed"
            emailmessage = "Please log in to your account to follow up on your application"
            emailfrom = 'applications@instarvid.com'
            # emailto = star.email
            star = Star.objects.get(pk=pk)
            emailto = star.owner.email
            send_mail(emailsubject, emailmessage, emailfrom, [emailto], fail_silently=False,)
            editedstar = form.save()
            context = {
                "message": "Profile Updated",
                "pk": pk,
                "star": Star.objects.get(pk=pk)
            }

        else:
            context = {
                "message": form.errors,
                "pk": pk,
            }
        return render(request, "stars/profile.html", context)


def specific_order(request, order_id):
    # make sure they are authenticated:
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    else:
        # see if the number of the order they are trying to view is actually an order:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        # check if the current user is the owner of the order
        if order.customer.id != request.user.id:
            return HttpResponse("You can only view orders that you have placed yourself.")
        try:
            # we only allow one video per order. No re-uploads for now.
            currentvideo = Video.objects.get(name=order_id)
            videofile = currentvideo.videofile
        except Video.DoesNotExist:
            # no previously uploaded video
            videofile = ""
    context = {
        'order_id': order_id,
        'videofile': videofile,
        'order_id': order_id,
        'messagefrom': order.messagefrom,
        'recipient': order.recipient,
        'custommessage': order.custommessage,
        'star': order.starbooked
    }
    return render(request, "orders/specific_order.html", context)


def orders(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return render(request, "users/login.html")
    user_id = request.user.id
    # get orders that were generated by the user:
    orders_placed = Order.objects.filter(customer=user_id).order_by('-completed')
    # requests = Order.objects.filter(starbooked__in(Star.objects.getstarbooked.owner.id=user_id)
    context = {
        "orders_placed": orders_placed,
    }
    return render(request, "orders/index.html", context)


def stardashboard(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    else:
        # does this user own any stars:
        owned_stars = Star.objects.filter(owner=request.user)
        # how many owned stars:
        number_of_stars = len(owned_stars)
        # for first star, get all the orders for that star:
        # owned_star_first = owned_stars.first()
        # owned_star_first_requests = Order.objects.filter(starbooked=owned_star_first)
        # for each star, get all the orders for that star:
        owned_star_requests = []
        for i in range(0, number_of_stars):
            # using in range instead of in owned_stars so we have an integer to make up the variable names:
            # .order_by('-completed') orders them by whether they are completed orders or open orders
            # reversed puts the completed ones on top
            ordr = reversed(Order.objects.filter(starbooked=owned_stars[i]).order_by('-completed'))
            owned_star_requests.append(ordr)
        context = {
            "owned_stars": owned_stars,
            "number_of_stars": number_of_stars,
            # "owned_star_first": owned_star_first,
            # "owned_star_first_requests": owned_star_first_requests,
            "owned_star_requests": owned_star_requests,
        }
        return render(request, "stars/stardashboard.html", context)


def upload(request, order_id):
    if not request.user.is_authenticated:
        return render(request, "users/login.html")
    else:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        # check if the current user is the same as owner
        if order.starbooked.owner.id != request.user.id:
            return HttpResponse("Please check your link, this page appears to be for a different user.")
        try:
            # we only allow one video per order. No re-uploads for now.
            currentvideo = Video.objects.get(name=order_id)
            videofile = currentvideo.videofile
            form = ""
        except Video.DoesNotExist:
            # no previously uploaded video
            videofile = ""
            form = VideoForm(request.POST or None, request.FILES or None,
                             initial={'name': order_id})
        if request.method == "POST":
            # they have just submitted a video
            # if post, try to display the video that was uploaded
            if form.is_valid():
                form.save()
                # set flag that the order is completed
                order.completed = True
                order.save()
                # send email to the customer that the video is ready:
                order_id_as_string = str(order_id)
                emailsubject = "Your video from " + order.starbooked.firstname + " " + \
                    order.starbooked.lastname + " is ready. Ref[" + order_id_as_string + "]"
                emailmessage = "Your video is ready to download or view. Please go to http://127.0.0.1:8000/order/" + \
                    order_id_as_string + " to get your video."
                emailfrom = 'orders@instarvid.com'
                emailto = order.customer.email
                send_mail(emailsubject, emailmessage, emailfrom, [emailto], fail_silently=False,)
                currentvideo = Video.objects.get(name=order_id)
                # get the URL of the video to show them what they have uploaded:
                videofile = currentvideo.videofile
                # don't show the form once they have uploaded a video:
                form = ""
            context = {'videofile': videofile,
                       'form': form,
                       'order_id': order_id,
                       'messagefrom': order.messagefrom,
                       'recipient': order.recipient,
                       'custommessage': order.custommessage,
                       }
        else:  # GET

            context = {'videofile': videofile,
                       'form': form,
                       'order_id': order_id,
                       'messagefrom': order.messagefrom,
                       'recipient': order.recipient,
                       'custommessage': order.custommessage,
                       }
        return render(request, 'stars/upload.html', context)


def admindashboard(request):
    # chedk if they are admin
    if request.user.is_superuser:
        context = {
            'approved': Star.objects.filter(status="APPROVED"),
            'pending': Star.objects.filter(status="PENDING"),
            'returned':  Star.objects.filter(status="RETURNED"),
            'resubmitted':  Star.objects.filter(status="RESUBMITTED"),
            'suspended':  Star.objects.filter(status="SUSPENDED"),
            'resubsuspended':  Star.objects.filter(status="RESUB_SUSPENDED"),
            'declined':  Star.objects.filter(status="DECLINED"),
            'resubdeclined': Star.objects.filter(status="RESUB_DECLINED"),
        }
        return render(request, 'stars/admindashboard.html', context)
    else:
        return HttpResponse("You do not have the right permissions to view this admin area.")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        # the following lines now working they check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "users/signup.html", {"message": "Username already exists"})
        user = User.objects.create_user(
            username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        return render(request, "users/login.html", {"message": "Account created. Please log in."})
    else:  # GET
        # if user is logged out
        if not request.user.is_authenticated:
            return render(request, "users/signup.html", {"message": None})
        # if user is logged in say "you are already logged in."
        return render(request, "users/signup.html", {"message": "You are already logged in"})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"warning": "Invalid credentials."})
    else:  # request method == GET
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"success": "Logged out."})
