from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.
def index(request): 
    allPosts = []
    posts = Blogpost.objects.values('title', 'post_id')
    # print('posts:', posts)
    # for post in posts:
    #     print(post.post_id)
    #     print(post.title)
    #     print(post.head0)
    #     print(post.chead0)

    _posts =  {post['title'] for post in posts}
    # print('_posts:', _posts)
    for _title in _posts:       
        post = Blogpost.objects.filter(title=_title)
        # print('post:', post)
        allPosts.append(post)
    
    # for item in allPosts:
    #     for i in item:
    #         print(i.title)

    params = {"allPosts": allPosts} 
    # print('allPosts:', allPosts)     
    # print('length(allPosts):', len(allPosts))

    myposts = Blogpost.objects.all()
    # print('myposts:', myposts)
    return render(request, 'blog/index.html', {'myposts': myposts})


def blogpost(request, id):    
    post = Blogpost.objects.filter(post_id=id)[0]     
    # post = Blogpost.objects.filter(post_id=id)[0]
    # post = Blogpost.objects.all()     
    # post = get_object_or_404(Blogpost, post_id=post_id) # retrieving the current post...

    # Get the next and previous blog posts based on publish_date (post_id)     
    # next_post = Blogpost.objects.filter(post_id=id).order_by('post_id').first()
    # previous_post = Blogpost.objects.filter(post_id=id).order_by('-post_id').first()
    # next_post = Blogpost.objects.all().order_by('post_id')#.first()
    # previous_post = Blogpost.objects.all().order_by('-post_id')#.first()

    # print('ascending post list:', Blogpost.objects.all().order_by('post_id'))
    # print('desending post list:', Blogpost.objects.all().order_by('-post_id'))

    # next_post_id = next_post.post_id if next_post else None
    # previous_post_id = previous_post.post_id if previous_post else None
    
    all_data = Blogpost.objects.all().order_by('post_id')    
    post_ids_ascending = []
    for item in all_data:
        item_data = Blogpost.objects.filter(title=item).values()[0]         
        post_ids_ascending.append(item_data['post_id'])
    
    prev_id, next_id = None, None
    if id!=post_ids_ascending[0] and id!=post_ids_ascending[-1]:
        prev_id, next_id = id-1, id+1
    elif id!=post_ids_ascending[0]:
        prev_id, next_id = id-1, None
    else:        
        prev_id, next_id = None, id+1
        
    context = {
        'post': post,
        'next_post': next_id,
        'previous_post': prev_id
    }
    return render(request, 'blog/blogpost.html', {'context': context})         
