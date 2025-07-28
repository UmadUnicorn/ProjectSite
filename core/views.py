import calendar
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')  # Или для Windows: 'Russian_Russia.1251'
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .models import Project, Event, EventPhoto
from .forms import EventHeaderForm, EventMetricsForm, ProjectForm, EventForm, EventPhotoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return redirect('project_list')

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'core/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'core/project_detail.html', {'project': project})

@login_required
def event_create(request, pk):
    project = get_object_or_404(Project, pk=pk)  # убрали проверку на owner
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.project = project
            event.owner = request.user  # добавили владельца мероприятия
            event.save()
            return redirect('project_detail', pk=pk)
    else:
        form = EventForm()
    return render(request, 'core/event_form.html', {'form': form, 'project': project})


@login_required
def calendar_view(request):
    events = []
    for project in Project.objects.filter(owner=request.user):
        for event in project.events.all():
            events.append({'title': event.name, 'date': event.date})
    return render(request, 'core/calendar.html', {'events': events})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Проверка прав доступа: только владелец или админ
    if project.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'core/project_form.html', {
        'form': form,
        'project': project,
    })


def event_detail(request, project_id, event_id):
    project = get_object_or_404(Project, pk=project_id)
    event = get_object_or_404(Event, pk=event_id, project=project)

    can_edit = (event.owner == request.user) or request.user.is_staff
    metrics = project.metrics
    actual_values = event.actual_metrics or {}

    # Обработка POST-запросов
    if request.method == 'POST':
        # Сохранение заголовка
        if 'edit_header' in request.POST:
            header_form = EventHeaderForm(request.POST, instance=event)
            if can_edit and header_form.is_valid():
                header_form.save()
                return redirect('event_detail', project_id=project.id, event_id=event.id)
        # Сохранение метрик
        elif 'upload_photo' not in request.POST:
            form = EventMetricsForm(request.POST, instance=event)
            if can_edit and form.is_valid():
                event.actual_metrics = form.cleaned_data['actual_metrics']
                event.save()
                return redirect('event_detail', project_id=project.id, event_id=event.id)

    # GET-запрос или невалидные POST
    form = EventMetricsForm(instance=event)
    header_form = EventHeaderForm(instance=event)
    photo_form = EventPhotoForm()

    # Обработка фото
    if request.method == 'POST' and 'upload_photo' in request.POST:
        if can_edit:
            photo_form = EventPhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                new_photo = photo_form.save(commit=False)
                new_photo.event = event
                new_photo.save()
                return redirect('event_detail', project_id=project.id, event_id=event.id)

    return render(request, 'core/event_detail.html', {
        'project': project,
        'event': event,
        'metrics': metrics,
        'form': form,
        'actual_values': actual_values,
        'header_form': header_form,
        'can_edit_header': can_edit,
        'can_edit_metrics': can_edit,
        'photo_form': photo_form,
        'photos': event.photos.all(),
    })

@login_required
def calendar_view(request):
    today = datetime.date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])

    events = Event.objects.filter(date__range=(first_day, last_day))

    # Группируем по дням
    events_by_day = {}
    for event in events:
        day = event.date.day
        events_by_day.setdefault(day, []).append(event)

    cal = calendar.Calendar(firstweekday=0)  # Пн — начало недели
    month_days = list(cal.itermonthdays4(year, month))  # (г, м, д, день_нед)

    context = {
        'year': year,
        'month': month,
        'month_name': first_day.strftime('%B').capitalize(),
        'days': month_days,
        'events_by_day': events_by_day,
        'day_names': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
    }

    return render(request, 'core/calendar_grid.html', context)

def custom_permission_denied(request, exception=None):
    return render(request, '403.html', status=403)