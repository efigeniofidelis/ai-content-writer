from django.shortcuts import render,redirect
from .forms import*
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from dashboard.functions import *
from django.contrib import messages





# Create your views here.
@login_required
def dashboard(request):
    emptyBlogs = []
    completeBlogs = []
    monthCount = 0

    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():
            #calculate the blog words
            blogWords = 0
            for section in sections:
                blogWords += int(section.wordCount)
                monthCount += int(section.wordCount)
            blog.wordCount = str(blogWords)
            blog.save()
            completeBlogs.append(blog)
        else:
            emptyBlogs.append(blog)

    context = {}
    context['numBlogs'] = len(completeBlogs)
    context['monthCount'] = str(monthCount) #update later
    context['countReset'] = '12 dec 2022'
    context['emptyBlogs'] = emptyBlogs
    context['completeBlogs'] = completeBlogs


    return render(request,'dashboard/home.html',context)

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



@login_required
def blogTopic(request):
    context = {}

    if request.method == 'POST':
        #retreiving the blog idea from a submitting form
        blogIdea = request.POST['blogIdea']
        #saving blog idea string in a session in order to use it later
        request.session['blogIdea'] = blogIdea
        keywords = request.POST['keywords']
        request.session['keywords'] = keywords
        audience = request.POST['audience']
        request.session['audience'] = audience

        blogTopics = generateBlogTopicIdeas(blogIdea,audience,keywords)
        if len(blogTopics) > 0:
            request.session['blogTopics'] = blogTopics
            return redirect('blog-section')
        else:
            messages.error(request,"oops we coounld not generate ideas for you")
            return redirect('blog-section')

    return render(request,'dashboard/blog_topic.html',context)




@login_required
def blogSection(request):
    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request,"start by making blog ideas")
        return redirect('blog_topic')

    context = {}
    context['blogTopics'] = request.session['blogTopics']

    return render(request,'dashboard/blog_section.html',context)


@login_required
def saveBlogTopic(request,blogTopic):
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session and 'blogTopics' in request.session:
            blog = Blog.objects.create(
            title = blogTopic,
            blogIdea  = request.session['blogIdea'],
            keywords = request.session['keywords'],
            audience = request.session['audience'],
            profile = request.user.profile)
            blog.save()

            blogTopics = request.session['blogTopics']
            blogTopics.remove(blogTopic)

            request.session['blogTopics'] = blogTopics
            return redirect('blog-section')
    else:
        return redirect('blog-topic')



@login_required
def createBlogFromTopic(request,uniqueId):
    context = {}
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request,"Blog not found")
        return redirect('dashboard')

    blogSections = generateBlogSections(blog.title,blog.audience,blog.keywords)

    if len(blogSections) > 0:
        request.session['blogSections'] = blogSections
        #adding sections into the context
        context['blogSections'] = blogSections
    else:
        messages.error(request,"oops we coounld not generate any blog sections for you for you")
        return redirect('blog-topic')
   
    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:

                #generating the blog section details
                section  = generateBlogSectionsDetails(blog.title,val,blog.audience,blog.keywords)

                #saving into database
                blogSec = BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog)
                blogSec.save()

        return redirect('view-generated-blog',slug= blog.slug)


    return render(request,'dashboard/select-blog-sections.html',context)







@login_required
def deleteblogTopic(request,uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            return redirect('dashboard')
        else:
            messages.error(request,"Access denied")
            return redirect('dashboard')
    except:
        messages.error(request,"blog not found")
        return redirect('dashboard')


@login_required
def useBlogTopic(request,blogTopic):
    context = {}
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session :
        blog = Blog.objects.create(
        title = blogTopic,
        blogIdea  = request.session['blogIdea'],
        keywords = request.session['keywords'],
        audience = request.session['audience'],
        profile = request.user.profile)
        blog.save()
        blogSections = generateBlogSections(blogTopic,request.session['audience'],request.session['keywords'])
    else:
        return redirect('blog-topic')


    if len(blogSections) > 0:
        request.session['blogSections'] = blogSections
        #adding sections into the context
        context['blogSections'] = blogSections
    else:
        messages.error(request,"oops we coounld not generate any blog sections for you for you")
        return redirect('blog-topic')
   
    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:

                #generating the blog section details
                section  = generateBlogSectionsDetails(blogTopic,val,request.session['audience'],request.session['keywords'])

                #saving into database
                blogSec = BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog)
                blogSec.save()

        return redirect('view-generated-blog',slug= blog.slug)


    return render(request,'dashboard/select-blog-sections.html',context)


@login_required
def viewGeneratedBlog(request,slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(request,"something went wrong")
        return redirect('blog-topic')


    #fetching the created sections

    blogSections = BlogSection.objects.filter(blog=blog)
    context = {}
    context['blog'] = blog
    context['blogSections']  = blogSections

    return render(request,'dashboard/view-generated-blog.html',context)




