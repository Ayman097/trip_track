from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from .models import Trip, Note

# Create your views here.
class HomeView(TemplateView):
    template_name = 'trip/index.html'

def trip_list(request):
    trips = Trip.objects.filter(owner=request.user)
    context = {
        'trips': trips
    }

    return render(request, 'trip/trip_list.html', context)

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    # '__all__' not Used here because owner is a foriegnkey so the user who logged in when he create this trip can't choose another user
    # so I need to specify the fields that user can fill
    fields = ['city', 'country', 'start_date', 'end_date']

    # Template named ==> modelname_form.html

    # Need to override this form valid to tell the owner will be the user who submit the form
    # without this will return error
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class TripDetailView(DetailView):
    model = Trip  # ==> ['city', 'country', 'start_date', 'end_date'] so here I did't know about note

    def get_context_data(self, **kwargs):
        # to get the actual content ==> trip itself
        context = super().get_context_data(**kwargs)
        # add context to note
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes
        return context


class NoteDetailView(DetailView):
    model = Note


class NoteListView(ListView):
    model = Note

    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner=self.request.user)
        return queryset
    

class NoteCreateView(CreateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = '__all__'

    def get_form(self):
        # Get the form
        form = super(NoteCreateView, self).get_form()
        # get trips for logged in user
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form
        

class NoteUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = '__all__'

    def get_form(self):
        # Get the form
        form = super(NoteUpdateView, self).get_form()
        # get trips for logged in user
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form
    


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')


class TripUpdateView(UpdateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']


class TripDeleteView(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')