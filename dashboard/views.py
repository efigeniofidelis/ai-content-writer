from django.shortcuts import render,redirect
from .forms import*
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from dashboard.functions import *
from django.contrib import messages
import time

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt





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
    context['monthCount'] = request.user.profile.monthlyCount #update later
    context['countReset'] = '12 dec 2022' #update later
    context['emptyBlogs'] = emptyBlogs
    context['completeBlogs'] = completeBlogs
    context['allowance'] =  checkCountAllowance(request.user.profile) ##will also use it to restrict user if not subscribe will not use different functionalities just add {%if not allowance%}{%endif%} on the specific button on template


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


    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:

                prevBlog = ''
                bSections = BlogSection.objects.filter(blog=blog).order_by('date_created')
                for sec in bSections:
                    prevBlog += sec.title + '\n'
                    prevBlog += sec.body.replace('<br','\n')
                prevBlog = '' ##will use it for rewirting blog in function

                #generating the blog section details
                section  = generateBlogSectionsDetails(blog.title,val,blog.audience,blog.keywords,request.user.profile)

                #saving into database
                blogSec = BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog)
                blogSec.save()
                time.sleep(2)

        return redirect('view-generated-blog',slug= blog.slug)
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
                prevBlog = ''
                bSections = BlogSection.objects.filter(blog=blog).order_by('date_created')
                for sec in bSections:
                    prevBlog += sec.title + '\n'
                    prevBlog += sec.body.replace('<br','\n')

                #generating the blog section details
                section  = generateBlogSectionsDetails(blogTopic,val,request.session['audience'],request.session['keywords'],request.user.profile)

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



@login_required
def checkCountAllowance(profile):
    if profile.subscribed:
        
        #user has a subscription
        type = profile.subscriptionType

        if type == 'free':
            max_limit = 5000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True

        
        elif type == 'starter':
            max_limit =40000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True

            

        elif type == 'advanced':
            return True

        else:
            return False
    else:
        max_limit = 5000
        if profile.monthlyCount:
            if int(profile.monthlyCount) < max_limit:
                return True
            else:
                return False
        else:
            return True



# product names are not saving yet just only working with sessions will save at end or when required.
@login_required
def productTopic(request):
    context = {}

    if request.method == 'POST':
        #retreiving the blog idea from a submitting form
        product_names = request.POST['product_names']
        #saving blog idea string in a session in order to use it later
        request.session['product_names'] = product_names
        seed_words = request.POST['seed_words']
        request.session['seed_words'] = seed_words


        productTopics = generateProductNames(product_names,seed_words)
        if len(productTopics) > 0:
            request.session['productTopics'] = productTopics
            return redirect('show_names')
        else:
            messages.error(request,"oops we coounld not generate ideas for you")
            return redirect('show_names')

    return render(request,'dashboard/product_names.html',context)



@login_required
def show_names(request):
    if 'productTopics' in request.session:
        pass
    else:
        messages.error(request,"start by making product names")
        return redirect('product_names')

    context = {}
    context['productTopics'] = request.session['productTopics']

    return render(request,'dashboard/show_names.html',context)




#for add creation


#for add creation save function needs to be created in future
@login_required
def generate_ads(request):
    context = {}

    if request.method == 'POST':
        #retreiving the product desc from a submitting form
        product_desc = request.POST['product_desc']
        #saving product desc string in a session in order to use it later
        request.session['product_desc'] = product_desc
        seed_words = request.POST['seed_words']
        request.session['seed_words'] = seed_words


        generate_ads = product_ads(product_desc,seed_words)
        if len(generate_ads) > 0:
            request.session['generate_ads'] = generate_ads
            return redirect('show_product_ads')
        else:
            messages.error(request,"oops we coounld not generate ideas for you")
            return redirect('show_product_ads')

    return render(request,'dashboard/product_ads.html',context)



@login_required
def show_ads(request):
    if 'productTopics' in request.session:
        pass
    else:
        messages.error(request,"start by making product names")
        return redirect('product_ads')

    context = {}
    context['generate_ads'] = request.session['generate_ads']

    return render(request,'dashboard/show_product_ads.html',context)



#keywords extractor


#keywords extractor save function need to be created
@login_required
def extract_keywords(request):
    context = {}

    if request.method == 'POST':
        #retreiving the product desc from a submitting form
        product_desc = request.POST['product_desc']
        #saving product desc string in a session in order to use it later
        request.session['product_desc'] = product_desc


        keywords = text_to_keywords(product_desc)
        if len(keywords) > 0:
            request.session['extract_keywords'] = keywords
            return redirect('show_text_to_keyword')
        else:
            messages.error(request,"oops we coounld not generate keywords for you")
            return redirect('show_text_to_keyword')

    return render(request,'dashboard/text_to_keywords.html',context)



@login_required
def show_keywords(request):
    if 'extract_keywords' in request.session:
        pass
    else:
        messages.error(request,"start by providing the text")
        return redirect('text_to_keyword')

    context = {}
    context['extract_keywords'] = request.session['extract_keywords']

    return render(request,'dashboard/show_text_to_keywords.html',context)












@login_required
def billing(request):

    context = {}
    return render(request,'dashboard/billing.html',context)


@require_POST
@csrf_exempt
def webhook(request):
    #verify taht the request is coming from paypal

    #check the type of event
    #1. subscription created
    #2. subscription cancellled
    return redirect('billing')