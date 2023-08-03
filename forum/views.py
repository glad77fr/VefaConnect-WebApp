from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .forms import UserRegisterForm, UserProfileForm
from django.core.mail import send_mail
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to the home page
        else:
            messages.error(request, 'Identifiant ou mot de passe invalide.')  # Add an error message
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
            gender = form.cleaned_data.get('gender')  # Extract gender from the form
            first_name = form.cleaned_data.get('first_name')  # Extract first_name from the form
            last_name = form.cleaned_data.get('last_name')  # Extract last_name from the form
            UserProfile.objects.create(user=user, bio=bio, photo=photo, gender=gender, first_name=first_name, last_name=last_name)  # Assign all the fields to the user profile
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

@login_required
def profile(request):
    if request.method == 'POST':
        # ici, vous devriez gérer la mise à jour du profil
        # par exemple, en utilisant un ModelForm pour UserProfile
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})