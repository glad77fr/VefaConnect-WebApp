from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .forms import UserRegisterForm, UserProfileForm
from django.core.mail import send_mail
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .models import Forum, ForumTheme, ForumPost, Reply
from django.shortcuts import render, get_object_or_404
from .models import ForumTheme
from django.views import View
from .forms import CreatePostForm
from django.views.generic import DetailView
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import ReplyModelForm
from django.core.paginator import Paginator

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

def general_forum_view(request):
    forum = get_object_or_404(Forum, name="General forum")
    themes = forum.themes.all().order_by('order')
    return render(request, 'general_forum.html', {'forum': forum, 'themes': themes})

class ForumThemeView(View):
    def get(self, request, topic_slug):
        topic = ForumTheme.objects.get(slug=topic_slug)
        posts = topic.posts.all().order_by('-date_posted')
        context = {
            'topic': topic,
            'posts': posts
        }
        return render(request, 'forum_theme_detail.html', context)
    
class CreatePostView(View):
    def get(self, request, *args, **kwargs):
        form = CreatePostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user.userprofile  # Attaching the UserProfile to the post, not the User
            new_post.theme = ForumTheme.objects.get(id=1)  # Replace with the appropriate logic to get the Theme
            new_post.save()
            return redirect('post_detail', pk=new_post.id)
        return render(request, 'create_post.html', {'form': form})

class PostDetailView(DetailView):
    model = ForumPost
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        replies = Reply.objects.filter(post=self.object).order_by('date_posted')
        paginator = Paginator(replies, 10)
        
        page = self.request.GET.get('page')
        context['replies'] = paginator.get_page(page)
        # Ajouter une instance du formulaire au contexte
        context['reply_form'] = ReplyModelForm()
        return context
    
def reply_to_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    user = request.user
    user_profile = user.userprofile  

    if request.method == "POST":
        form = ReplyModelForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            reply = Reply.objects.create(user=user_profile, post=post, content=content)

            html = render_to_string('path_to_reply_template.html', {'reply': reply})

            return JsonResponse({'reply_html': html})
        if not form.is_valid(): 
            print(form.errors)

    # En cas d'erreur, vous pouvez retourner une réponse d'erreur 
    # (cela dépend de la façon dont vous souhaitez gérer les erreurs côté client)
    return JsonResponse({'error': 'Invalid form data.'}, status=400)

def load_more_replies(request, post_id, page):
    post = get_object_or_404(ForumPost, id=post_id)
    replies = Reply.objects.filter(post=post)
    
    paginator = Paginator(replies, 10)
    current_page_replies = paginator.get_page(page)
    
    html = render_to_string('path_to_replies_template.html', {'replies': current_page_replies})

    return JsonResponse({'replies_html': html})




