
from .models import *


def ogeler(request):
    categories = Category.objects.all()
    return ({'categories':categories})