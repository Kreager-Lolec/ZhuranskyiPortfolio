from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from .models import Project
from .forms import ProjectForm, ContactForm


class HomeView(ListView):
    """
    View for the homepage displaying all projects
    """
    model = Project
    template_name = 'portfolio/home.html'
    context_object_name = 'projects'


class AboutView(ListView):
    """
    View for the about page
    """
    model = Project
    template_name = 'portfolio/about.html'


class ContactView(FormView):
    """
    View for the contact page and handling contact form submissions
    """
    template_name = 'portfolio/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = f"""
        From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>
        
        {form.cleaned_data['message']}
        """
        from_email = form.cleaned_data['email']
        recipient_list = ['juranskiy59@gmail.com']
        
        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(self.request, "Your message has been sent successfully!")
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except Exception as e:
            messages.error(self.request, f"An error occurred while sending your message: {str(e)}")
        
        return super().form_valid(form)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new project
    """
    login_url = '/login/'
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/add_project.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Handle successful form submission and redirect to home"""
        messages.success(self.request, "Project added successfully!")
        return super().form_valid(form)
        
    def form_invalid(self, form):
        """Handle invalid form submission"""
        messages.error(self.request, "Error adding project. Please check the form.")
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            # For faster submission, process only necessary fields
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()  # Save many-to-many relationships if any
            messages.success(self.request, "Project added successfully!")
            return redirect('home')
        else:
            return self.form_invalid(form)


class ProjectDetailView(DetailView):
    """
    View for displaying a single project
    """
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing project
    """
    login_url = '/login/'
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/add_project.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Project updated successfully!")
        return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, "Error updating project. Please check the form.")
        return super().form_invalid(form)
        
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            # For faster submission, process only necessary fields
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()  # Save many-to-many relationships if any
            messages.success(self.request, "Project updated successfully!")
            return redirect('home')
        else:
            return self.form_invalid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a project
    """
    login_url = '/login/'
    model = Project
    success_url = reverse_lazy('home')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Project deleted successfully!")
        return super().delete(request, *args, **kwargs)
