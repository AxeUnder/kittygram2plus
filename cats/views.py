from rest_framework import viewsets, permissions
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .throttling import WorkingHoursRateThrottle

from .permissions import OwnerOrReadOnly

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    # Устанавливаем разрешение
    permission_classes = (OwnerOrReadOnly,)
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle,)
    # Даже если на уровне проекта установлен PageNumberPagination
    # Для котиков будет работать LimitOffsetPagination
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
