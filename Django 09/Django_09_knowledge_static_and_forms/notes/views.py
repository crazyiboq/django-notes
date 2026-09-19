from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render

from . import data
from .forms import NoteForm, ContactForm


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'notes/home.html')


def about(request: HttpRequest) -> HttpResponse:
    context = {
        'project_name':'Knowledge Hub',
        'author':'Nadir Zamanov',
    }
    return render(request, 'notes/about.html', context)


def notes_list(request: HttpRequest) -> HttpResponse:
    notes = data.list_notes()
    return render(request, 'notes/notes_list.html', {'notes': notes})


def note_detail(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = data.get_note(note_id)
    return render(request, 'notes/note_detail.html', {'note': note})


def note_create(request: HttpRequest) -> HttpResponse:
    note = ""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = request.session.get('notes', [])
            notes.append(
                {
                    'title': form.cleaned_data['title'],
                    'content': form.cleaned_data['content'],
                    'tags': form.cleaned_data['tags'],
                    'category': form.cleaned_data['category'],
                })
            request.session['notes'] = notes

            if not form.cleaned_data['title']:
                error = 'Title is required'
            else:
                data.create_note(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    category=form.cleaned_data['category'],
                    tags= form.cleaned_data['tags'].split(),
            )
            return redirect('notes_list')
    else:
        form = NoteForm()

    return render(request, 'notes/note_create.html', {
        'form': form,
    })


def note_edit(request: HttpRequest, note_id:int) -> HttpResponse:
    note = data.get_note(note_id)
    if request.method == 'POST':
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        category = request.POST.get('category', "")
        tags = request.POST.get('tag')
        data.update_note(
            note_id=note_id,
            title=title.strip(),
            content=content.strip(),
            category=category.strip(),
            tags= tags.split() or None
        )
        return redirect('notes_list')

    return render(request, 'notes/note_edit.html', {'note': note})

def note_delete(request: HttpRequest, note_id:int) -> HttpResponse:
    note = data.get_note(note_id)
    if request.method == 'POST':
        data.delete_note(note_id)
        return redirect('notes_list')
    return render(request, 'notes/note_delete.html', {'note': note})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]

            return render(
                request,
                "notes/contact_success.html",
                {"name": name}
            )
    else:
        form = ContactForm()

    return render(
        request,
        "notes/contact.html",
        {"form": form}
    )