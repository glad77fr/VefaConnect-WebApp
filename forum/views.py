from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .forms import UserRegisterForm
from django.core.mail import send_mail

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to the home page
        else:
            return render(request, 'login_register.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login_register.html')

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            bio = form.cleaned_data.get('bio')
            photo = form.cleaned_data.get('photo')
            UserProfile.objects.create(user=user, bio=bio, photo=photo)
            login(request, user)

            # Send confirmation email
            # send_mail(
            #     'Welcome to our site!',
            #     'Thanks for signing up!',
            #     'from@example.com',
            #     [user.email],
            #     fail_silently=False,
            # )

            return render(request, 'register_validation.html') # Remplacez par le nom de votre template
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Envoyer l'email ici.
        send_mail(
            'Message de ' + name,  # sujet
            message,  # message
            email,  # de l'email
            ['your-email@example.com'],  # à l'email
        )

        return redirect('nom_de_lurl_de_confirmation')

    return render(request, 'contact.html')