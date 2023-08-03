from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FollowedProgramForm
from django.db.models import Q
from .models import RealEstateProgram
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import RealEstateProgram, FollowedProgram
from forum.models import UserProfile
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    return render(request, 'home.html')

def ProgramSearchView(request):
    query = request.GET.get('q', '')
    search_performed = bool(query)
    if search_performed:
        results = RealEstateProgram.objects.filter(Q(name__icontains=query) | Q(address__city__name__icontains=query))
    else:
        results = RealEstateProgram.objects.order_by('?')[:10]

    title = "Résultats de recherche" if search_performed else "Programmes"
    return render(request, 'program_search_results.html', {'results': results, 'query': query, 'search_performed': search_performed, 'title': title})

class ProgramDetailView(DetailView):
    model = RealEstateProgram
    template_name = 'program_detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.userprofile
            program_is_followed = FollowedProgram.objects.filter(user_profile=user_profile, real_estate_program=self.object).exists()
            context['program_is_followed'] = program_is_followed
        else:
            context['program_is_followed'] = False
        return context


@login_required
def follow_program_view(request, program_id):
    program = RealEstateProgram.objects.get(id=program_id)
    user_profile = request.user.userprofile
    if not FollowedProgram.objects.filter(user_profile=user_profile, real_estate_program=program).exists():
        return redirect('program_register', program_id=program.id)  # redirect to the form view
    else:
        return redirect('program_details', program_id=program.id)  # if the user already follows the program, redirect back to the program details page
    
class FollowedProgramView(FormView):
    template_name = 'program_register.html'
    form_class = FollowedProgramForm
    success_url = reverse_lazy('followed-program-confirmation')  # Définir success_url ici


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.program = RealEstateProgram.objects.get(id=self.kwargs['program_id'])
        user = self.request.user.userprofile
        kwargs.update({'program': self.program, 'user': user})
        return kwargs

    def form_valid(self, form):
        form.save()
        # Here you can handle your form after it has been validated
        # For example, you can save the instance of your FollowedProgramForm

        # Then, render your template with the program name in the context
        # Store the program ID in the session
        self.request.session['program_id'] = self.program.id
        return super().form_valid(form) 

class FollowedProgramConfirmationView(TemplateView):
    template_name = 'followedprogram_confirmation.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the program ID from the session
        program_id = self.request.session.get('program_id')
            
        # If a program ID was stored in the session, get the corresponding program
        if program_id is not None:
            program = RealEstateProgram.objects.get(id=program_id)
            context['program'] = program
    
        return context