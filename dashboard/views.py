from django.shortcuts import render,redirect
from .forms import*
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from dashboard.functions import *
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):

    context = {}
    return render(request,'dashboard/home.html',{})

@login_required
def profile(request):
    context={}

    if request.method == 'GET':
        form  = ProfileForm(instance = request.user.profile,user=request.user)
        image_form = ProfileImageForm(instance = request.user.profile)
        context['form'] = form
        context['image_form'] = image_form
        return render(request, 'dashboard/profile.html', context)

    if request.method == 'POST':
        image_form = ProfileImageForm(request.POST,request.FILES,instance = request.user.profile)
        form  =  ProfileForm(request.POST,instance = request.user.profile)

        if form.is_valid():
            form.save()
            return redirect('profile')
        if image_form.is_valid():
            image_form.save()
            return redirect('profile')



    return render(request,'dashboard/profile.html',context)




def blogTopic(request):
    context = {}

    if request.method == 'POST':
        blogIdea = request.POST['blogIdea']
        keywords = request.POST['keywords']

        blogTopics = generateBlogTopicIdeas(blogIdea,keywords)
        if len(blogTopics) > 0:
            request.session['blogTopics'] = blogTopics
            return redirect('blog-section')
        else:
            messages.error(request,"oops we coounld not generate ideas for you")
            return redirect('blog-section')

    return render(request,'dashboard/blog_topic.html',context)





def blogSection(request):
    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request,"start by making blog ideas")
        return redirect('blog_topic')

    context = {}
    context['blogTopics'] = request.session['blogTopics']

    return render(request,'dashboard/blog_section.html',context)

