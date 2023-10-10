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
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from website.models import RealEstateProgram
from django.http import JsonResponse


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
    forum = get_object_or_404(Forum, name="Forum Général")
    themes = forum.themes.all().order_by('order')
    return render(request, 'general_forum.html', {'forum': forum, 'themes': themes})


class ForumThemeView(View):
    def get(self, request, topic_slug, program_slug=None):
        program = None
        if program_slug:
            program = RealEstateProgram.objects.get(slug=program_slug) 
        
        program_exists = bool(program)
        topic = ForumTheme.objects.get(slug=topic_slug)
        
        # Récupérer tous les posts du thème
        posts_all = topic.posts.all()
        
        # Si un programme est spécifié, filtrez les posts en fonction de ce programme
        if program:
            posts_all = posts_all.filter(real_estate_program=program)
        
        posts_all = posts_all.order_by('-date_posted')

        # Pagination
        paginator = Paginator(posts_all, 10)  # Show 10 posts per page
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {
            'program': program,
            'topic': topic,
            'posts': posts,
            'program_exists': program_exists,
        }
        return render(request, 'forum_theme_detail.html', context)


@method_decorator(login_required(login_url='access_denied'), name='dispatch')
class CreatePostView(View):
    def get(self, request, topic_slug ,program_slug=None, *args, **kwargs):
        
        # Initialize the form with the real_estate_program field if program_pk is provided
        initial_data = {}
        if program_slug:
            program = get_object_or_404(RealEstateProgram, slug=program_slug)
            initial_data['real_estate_program'] = program
        initial_data['theme'] = get_object_or_404(ForumTheme, slug=topic_slug)
   

        form = CreatePostForm(initial=initial_data)
        return render(request, 'create_post.html', {'form': form})

    def post(self, request, topic_slug, program_slug=None, *args, **kwargs):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Message de débogage
            new_post = form.save(commit=False)
            new_post.user = request.user.userprofile  # Attaching the UserProfile to the post, not the User
            new_post.theme = ForumTheme.objects.get(slug=topic_slug)  # Replace with the appropriate logic to get the Theme
            if program_slug:  # Assign the program if its pk is provided
                new_post.real_estate_program = get_object_or_404(RealEstateProgram, slug=program_slug)
            new_post.save()
             # Redirecting based on the presence of program_slug
            if program_slug:
                return redirect('program_post_detail', program_slug=program_slug, topic_slug=topic_slug, post_slug=new_post.slug)
            else:
                return redirect('general_post_detail', topic_slug=topic_slug, post_slug=new_post.slug)
        else:
            print("Form is NOT valid", form.errors)  # Message de débogage
        return render(request, 'create_post.html', {'form': form})

class PostDetailView(DetailView):
    model = ForumPost
    template_name = 'post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'         
    slug_url_kwarg = 'post_slug' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_slug = self.kwargs['topic_slug']
        post_slug = self.kwargs['post_slug']
        program_slug = self.kwargs.get('program_slug')


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

     # Vérifier si l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return HttpResponse(status=401)  # Code 401 pour "non autorisé"
    
    user_profile = user.userprofile


    if request.method == "POST":
        form = ReplyModelForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            reply = Reply.objects.create(user=user_profile, post=post, content=content)

            html = render_to_string('reply_template.html', {'reply': reply})

            return JsonResponse({'reply_html': html})
        if not form.is_valid(): 
            print(form.errors)

    return JsonResponse({'error': 'Invalid form data.'}, status=400)

def load_more_replies(request, post_id, page):
    post = get_object_or_404(ForumPost, id=post_id)
    replies = Reply.objects.filter(post=post)
    
    paginator = Paginator(replies, 10)
    current_page_replies = paginator.get_page(page)
    
    html = render_to_string('reply_template.html', {'replies': current_page_replies})

    return JsonResponse({'replies_html': html})

def access_denied(request):
    return render(request, 'access_denied.html')

class ProgramForumView(View):
    def get(self, request, program_slug):
        program =  program = get_object_or_404(RealEstateProgram, slug=program_slug)

        # Récupération du forum ayant pour nom "Forum programmes"
        forum_programmes = Forum.objects.get(name="Forum programmes")

        # Récupération des thèmes du forum spécifié
        themes = ForumTheme.objects.filter(forum=forum_programmes).order_by('order')

        # Calcul du nombre de posts et de réponses pour chaque thème, spécifiques à ce programme immobilier
        for theme in themes:
            theme.post_count_program = ForumPost.objects.filter(theme=theme, real_estate_program=program).count()
            theme.reply_count_program = Reply.objects.filter(post__theme=theme, post__real_estate_program=program).count()

            # Trouver la date du post le plus récent pour ce thème
            latest_post_date = ForumPost.objects.filter(theme=theme, real_estate_program=program).order_by('-date_posted').values_list('date_posted', flat=True).first()

            # Trouver la date de la réponse la plus récente pour ce thème
            latest_reply_date = Reply.objects.filter(post__theme=theme, post__real_estate_program=program).order_by('-date_posted').values_list('date_posted', flat=True).first()

            # Retenir la date la plus récente comme la "dernière activité" du thème
            theme.last_activity_date = max(filter(None, [latest_post_date, latest_reply_date]), default=None)


        context = {
            'real_estate_program': program,
            'themes': themes
        }
        return render(request, 'program_forum.html', context)

@login_required
def upvote_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    user = request.user
    
    # Vérifier si l'utilisateur a déjà voté
    if user in reply.upvoted_users.all():
        # Si c'est le cas, retirez le vote
        reply.upvoted_users.remove(user)
        upvoted = False
    else:
        # Sinon, ajoutez le vote
        reply.upvoted_users.add(user)
        upvoted = True

    return JsonResponse({
        'upvoted': upvoted,
        'count': reply.upvotes_count  # Assurez-vous d'avoir une propriété ou une méthode 'upvotes_count' sur le modèle 'ForumReply'
    })