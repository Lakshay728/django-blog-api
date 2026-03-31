from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import PostSerializer

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'blog/login.html', {'error': 'Invalid username or password!'})
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def create_post_page(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(
            title=title,
            content=content,
            image=image,
            owner=request.user
        )
        return redirect('/')
    return render(request, 'blog/create_post.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        search = request.query_params.get('search', None)
        if search:
            posts = posts.filter(title__icontains=search) | posts.filter(content__icontains=search)
        owner = request.query_params.get('owner', None)
        if owner:
            posts = posts.filter(owner__username=owner)
        ordering = request.query_params.get('ordering', '-created_at')
        posts = posts.order_by(ordering)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if post.owner != request.user:
            return Response({'error': 'You can only edit your own posts!'}, status=403)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        if post.owner != request.user:
            return Response({'error': 'You can only delete your own posts!'}, status=403)
        post.delete()
        return Response({'message': 'Post deleted!'}, status=204)