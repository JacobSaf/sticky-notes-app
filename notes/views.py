from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm


def note_list(request):
    """
    Display all sticky notes in the application.
    This view is publicly accessible.
    """
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})


def add_note(request):
    """
    Handle the creation of a new sticky note.
    Accepts POST requests to save a note and 
    GET requests to display the form. 
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})


def edit_note(request, note_id):
    """
    Handles editing the sticky note. 
    """
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

def delete_note(request, note_id):
    """
    Delete a specific sticky note by its ID.
    Redirects back to notes list after deletion.
    """
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/delete_note.html', {'note': note})

