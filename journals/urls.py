from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_list, name='journal_list'),
    path('journal/<int:journal_id>/', views.journal_detail, name='journal_detail'),
    path('journal/create/', views.create_journal, name='create_journal'),
    path('journal/<int:journal_id>/entry/', views.add_entry, name='add_entry'),
    path('journal/<int:journal_id>/entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('journal/<int:journal_id>/delete/', views.delete_journal, name='delete_journal'),
    path('journal/<int:journal_id>/share/', views.share_journal, name='share_journal'),
    path('journal/<int:journal_id>/export/md/', views.export_markdown, name='export_markdown'),
    path('journal/<int:journal_id>/export/pdf/', views.export_pdf, name='export_pdf'),
    path('heatmap/', views.activity_heatmap, name='activity_heatmap'),
    path('register/', views.register, name='register'),
    path('public/', views.public_journals, name='public_journals'),

]