from rest_framework import viewsets, permissions
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .pagination import CatsPagination

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
    # Вот он наш собственный класс пагинации с page_size=20
    pagination_class = CatsPagination

    def get_queryset(self):
        queryset = Cat.objects.all()
        color = self.request.query_params.get('color')
        if color is not None:
            #  через ORM отфильтровать объекты модели Cat
            #  по значению параметра color, полученного в запросе
            queryset = queryset.filter(color=color)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
