from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Project(models.Model):
    # 1. О чём проект
    title = models.CharField("Название проекта", max_length=200)
    description = models.TextField("Описание проекта")
    background = models.TextField("Предпосылки проекта")
    status = models.CharField("Статус проекта", max_length=100)
    relevance = models.TextField("Актуальность")

    # 2. Цель и метрики
    goal = models.TextField("Цель проекта")
    results = models.TextField("Результаты и продукты проекта")

    # 3. Команда
    team = models.JSONField("Роли и телефоны", default=list)

    # 4. Стейкхолдеры
    audience = models.TextField("Целевая аудитория")
    event_type = models.CharField("Вид мероприятия", max_length=200)

    # 5. Риски
    risks = models.JSONField("Риски и их влияния", default=list)

    # 6. Ресурсы
    material_resources = models.TextField("Материальные ресурсы")
    non_material_resources = models.TextField("Нематериальные ресурсы")

    # Метрики
    metrics = models.JSONField("Метрики и цели", default=list)

    # Системные поля
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    project = models.ForeignKey('Project', related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField("Дата и время проведения")  # было DateField
    actual_metrics = models.JSONField("Фактические значения", default=dict, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} — {self.date.strftime('%d.%m.%Y %H:%M')}"

class EventPhoto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='event_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Фото для {self.event.title} ({self.uploaded_at})"
