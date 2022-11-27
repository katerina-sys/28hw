import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category
from ads.permissions import IsOwnerAdOrStaff
from ads.serializers import AdSerializer, AdDetailSerializer, AdListSerializer, AdCreateSerializer
from homework27.settings import TOTAL_ON_PAGE
from users.models import User


def root(request):
    return JsonResponse({'status': 'ok'})


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    default_serializer = AdSerializer
    serializer_classes = {
        'retrieve': AdDetailSerializer,
        'list': AdListSerializer,
        'create': AdCreateSerializer
    }

    default_permission = [AllowAny()]
    permissions = {
        'create': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsOwnerAdOrStaff()],
        'partial_update': [IsAuthenticated(), IsOwnerAdOrStaff()],
        'destroy': [IsAuthenticated(), IsOwnerAdOrStaff()],
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        return super().list(self, request, *args, **kwargs)


# class AdListView(ListView):
# model = Ad

# def get(self, request, *args, **kwargs):
#   super().get(request, *args, **kwargs)
#   self.object_list = self.object_list.order_by('-price')
#   paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
#   page = request.GET.get('page')
#   obj = paginator.get_page(page)
#  response = {}
#  items_list = [{
#      'id': ad.pk,
#      'name': ad.name,
#      'author': ad.author.first_name,
#      'price': ad.price,
#      'category': ad.category.name,
#      'description': ad.description,
#      'is_published': ad.is_published,
#      'image': ad.image.url if ad.image else None} for ad in obj]
#  response['items'] = items_list
#  response['total'] = self.object_list.count()
#  response['num_pages'] = paginator.num_pages
#  return JsonResponse(response, safe=False)


# @method_decorator(csrf_exempt, name='dispatch')
# class AdCreateView(CreateView):
# model = Ad
# fields = ["name"]

# def post(self, request, *args, **kwargs):
#    data = json.loads(request.body)
#    author = get_object_or_404(User, username=data['author'])
#    category = get_object_or_404(Category, name=data['category'])

#    ad = Ad.objects.create(name=data['name'],
#                           author=author,
#                           category=category,
#                           price=data['price'],
#                           description=data['description'],
#                           is_published=data['is_published'])
#    return JsonResponse({
#        'id': ad.pk,
#        'name': ad.name,
#        'author': ad.author.username,
#        'price': ad.price,
#        'description': ad.description,
#        'category': ad.category.name,
#        'is_published': ad.is_published
#    }, safe=False)


# class AdDetailView(DetailView):
# model = Ad

# def get(self, *args, **kwargs):
#    ad = self.get_object()
#     return JsonResponse({
#        'id': ad.pk,
#        'name': ad.name,
#        'author': ad.author.username,
#        'category': ad.category.name,
#        'price': ad.price,
#        'description': ad.description,
#        'is_published': ad.is_published,
#         'image': ad.image.url if ad.image else None}, safe=False)


# @method_decorator(csrf_exempt, name='dispatch')
# class AdUpdateView(UpdateView):
# model = Ad
# fields = ["name"]

# def patch(self, request, *args, **kwargs):
#    super().post(request, *args, **kwargs)
#    data = json.loads(request.body)
#    # author = get_object_or_404(User, data['author'])
#    # category = get_object_or_404(Category, data['category'])
#    if 'name' in data:
#        self.object.name = data['name']
#    if 'price' in data:
#        self.object.price = data['price']
#    if 'description' in data:
#        self.object.description = data['description']
#    if 'is_published' in data:
#        self.object.is_published = data['is_published']

#    self.object.save()
#    return JsonResponse({
#        'id': self.object.pk,
#        'name': self.object.name,
#        'author': self.object.author,
#        'price': self.object.price,
#        'description': self.object.description,
#        'is_published': self.object.is_published, }, safe=False)


# @method_decorator(csrf_exempt, name='dispatch')
# class AdDeleteView(DeleteView):
# model = Ad
# success_url = "/"

# def delete(self, request, *args, **kwargs):
#   super().delete(request, *args, **kwargs)
#    return JsonResponse({'status': 'ok'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImage(UpdateView):
    model = Ad
    fields = ['name']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'author': self.object.author,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None}, safe=False)
