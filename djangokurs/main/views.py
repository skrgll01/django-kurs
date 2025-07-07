from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def index(request):
    courses = Course.objects.all()
 
    return render(request,'main/index.html',{'courses':courses})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"İletişim Formu - {name}"
        body = f"""
Gönderen: {name}
E-posta: {email}

Mesaj:
{message}
"""

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,  # kendi mailin
                [settings.DEFAULT_FROM_EMAIL],  # alıcı (kendi mailin)
                fail_silently=False,
            )
            messages.success(request, "Mesajınız başarıyla gönderildi.")
        except Exception as e:
            messages.error(request, f"Hata oluştu: {e}")

        # Formu gönderen sayfaya geri döndür (referer)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # GET isteği için fallback (genellikle gerekmez footer formu için)
    return render(request, 'main/layout.html')
def search(request):
    q = request.GET.get('q')
    
    courses = Course.objects.filter(isActive=True,title__contains=q)

    return render(request,'main/index.html',{'courses':courses})

def getCategories(request,slug):
    courses = Course.objects.filter(isActive=True,categories__slug = slug)

    return render(request,'main/index.html',{'courses':courses})


def getCourses(request,slug):
    courses = Course.objects.filter(isActive=True,slug = slug)
    return render(request,'main/courses.html',{'courses':courses})

@login_required
def KursEkle(request):
    if request.method == 'POST':
        form = kursForm(request.POST, request.FILES)
        video_form = VideoUploadForm(request.POST, request.FILES)

        if form.is_valid() and video_form.is_valid():
            course = form.save()

            # Videoları kaydet ve ilişkilendir
            for file in request.FILES.getlist('videos'):
                video_instance = Video.objects.create(video=file)
                course.videos.add(video_instance)

            return redirect('/')
    else:
        form = kursForm()
        video_form = VideoUploadForm()

    return render(request, 'main/kursekle.html', {
        'form': form,
        'video_form': video_form
    })
@login_required
def icerik(request, id):
    video = get_object_or_404(Video, id=id)
    # Videoya dahil olan kursları al (ManyToMany olduğu için)
    courses = Course.objects.filter(videos=video)
    course = courses.first()  # Genelde 1 tane olur
    videolar = course.videos.all() if course else []

    context = {
        'video': video,
        'course': course,
        'videolar': videolar,
    }
    return render(request, 'main/icerik-ozel.html', context)


