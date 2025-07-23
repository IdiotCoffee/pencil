from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Journal, Entry, Permission
from django.utils import timezone
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import messages
import json
from datetime import datetime
from django.contrib.auth import login
from .forms import RegisterForm
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import markdown
from .models import Journal

def public_journals(request):
    journals = Journal.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'journals/public_list.html', {'journals': journals})

@login_required
def journal_list(request):
    user = request.user

    # Journals owned by the current user
    owned_journals = Journal.objects.filter(owner=user)

    # Journals shared with the current user
    shared_permissions = Permission.objects.filter(user=user).select_related('journal__owner')
    shared_journals = []
    for perm in shared_permissions:
        journal = perm.journal
        journal.shared_by = journal.owner  # attach custom attribute for template use
        shared_journals.append(journal)

    # Combine and send to template
    journals = list(owned_journals) + shared_journals

    return render(request, 'journals/journal_list.html', {
        'journals': journals,
        'user': user
    })
@login_required
@login_required
@login_required
def journal_detail(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)

    # ✅ Allow if user is owner, has permission, or it's public
    has_access = (
        journal.owner == request.user or
        journal.permissions.filter(user=request.user).exists() or
        journal.is_public
    )
    if not has_access:
        return HttpResponse("Unauthorized", status=401)

    entries = journal.entries.order_by('-created_at')

    # ✅ Can edit only if owner or has edit permission (public viewers can't)
    can_edit = (
        journal.owner == request.user or
        journal.permissions.filter(user=request.user, can_edit=True).exists()
    )

    return render(request, 'journals/journal_detail.html', {
        'journal': journal,
        'entries': entries,
        'can_edit': can_edit
    })

@login_required
def create_journal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        is_public = request.POST.get('is_public') == 'on'
        journal = Journal.objects.create(title=title, owner=request.user, is_public=is_public)
        return redirect('journal_detail', journal_id=journal.id)
    return render(request, 'journals/create_journal.html')

@login_required

def add_entry(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)

    # Check if user is owner or has edit permissions
    if not (journal.owner == request.user or journal.permissions.filter(user=request.user, can_edit=True).exists()):
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')

        # Create entry, now with user
        entry = Entry.objects.create(
            journal=journal,
            content=content,
            media=media,
            user=request.user  # ← Fix is here
        )

        return redirect('journal_detail', journal_id=journal.id)

    return render(request, 'journals/add_entry.html', {'journal': journal})


@login_required
def delete_entry(request, journal_id, entry_id):
    journal = get_object_or_404(Journal, id=journal_id)
    entry = get_object_or_404(Entry, id=entry_id, journal=journal)
    if not (journal.owner == request.user or journal.permissions.filter(user=request.user, can_edit=True).exists()):
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry deleted successfully.")
        return redirect('journal_detail', journal_id=journal.id)
    return render(request, 'journals/delete_entry.html', {'journal': journal, 'entry': entry})

@login_required
def delete_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if journal.owner != request.user:
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        journal.delete()
        messages.success(request, "Journal deleted successfully.")
        return redirect('journal_list')
    return render(request, 'journals/delete_journal.html', {'journal': journal})

@login_required
def share_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if journal.owner != request.user:
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        username = request.POST.get('username')
        can_edit = request.POST.get('can_edit') == 'on'
        try:
            user = User.objects.get(username=username)
            Permission.objects.update_or_create(journal=journal, user=user, defaults={'can_edit': can_edit})
            messages.success(request, f"Shared with {username}")
        except User.DoesNotExist:
            messages.error(request, "User not found")
        return redirect('share_journal', journal_id=journal.id)
    permissions = journal.permissions.all()
    return render(request, 'journals/share_journal.html', {'journal': journal, 'permissions': permissions})

@login_required
def export_markdown(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if not (journal.owner == request.user or journal.permissions.filter(user=request.user).exists()):
        return HttpResponse("Unauthorized", status=401)
    entries = journal.entries.order_by('created_at')
    content = f"# {journal.title}\n\n"
    for entry in entries:
        content += f"## {entry.created_at.strftime('%Y-%m-%d %H:%M')}\n{entry.content}\n\n"
    response = HttpResponse(content, content_type='text/markdown')
    response['Content-Disposition'] = f'attachment; filename="{journal.title}.md"'
    return response

@login_required
def export_pdf(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if not (journal.owner == request.user or journal.permissions.filter(user=request.user).exists()):
        return HttpResponse("Unauthorized", status=401)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, journal.title)
    y = 700
    for entry in journal.entries.order_by('created_at'):
        p.drawString(100, y, f"{entry.created_at.strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        for line in entry.content.split('\n'):
            if y < 50:
                p.showPage()
                y = 750
            p.drawString(100, y, line[:80])  # Truncate for simplicity
            y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{journal.title}.pdf"'
    return response

@login_required
def activity_heatmap(request):
    entries = Entry.objects.filter(journal__owner=request.user).values('created_at__date').annotate(count=Count('id'))
    heatmap_data = {int(datetime.combine(entry['created_at__date'], datetime.min.time()).timestamp()): entry['count'] for entry in entries}
    return render(request, 'journals/heatmap.html', {'heatmap_data': json.dumps(heatmap_data)})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('journal_list')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



