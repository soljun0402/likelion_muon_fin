import secrets
import requests
import xmltodict
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import *
import decimal, sys, os
from django.db.models import Q
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import parserim
from secrets import SECRET
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all()[:3]
    return render(request, 'home.html', {'posts':posts})

def musical_list(request):
    all_product = parserim.parse_product()
    products = list(all_product)
    #입력 파라미터      
    page = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw', '') #검색어

    # 검색기능
    tmp_product = Product.objects.all()
    if kw:
          tmp_product = tmp_product.filter(
                Q(title__icontains=kw) 
          ).distinct()
          tmp_product = tmp_product.values()
          tmp = []
          for j in range(len(tmp_product)):
                for i in range(len(all_product)):
                      if tmp_product[j]['pID']==products[i]['mt20id']:
                            tmp.append(products[i])
          products = tmp

    # 페이징처리
    paginator = Paginator(products, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    ctx = {
      'products': page_obj, 
      'page': page, 
      'kw': kw,
      }
    return render(request, 'musical_list.html', ctx)

def musical_detail(request, pID):
    product = get_object_or_404(Product, pID=pID)
    # 평점 계산
    if request.method == 'POST':
      tmpS1 = product.score1
      tmpS2 = product.score2
      tmpS3 = product.score3
      tmpS4 = product.score4
      tmp = product.review_count
      product.review_count = tmp + 1
      product.score1 = (tmpS1*tmp + decimal.Decimal(request.POST['score1']))/product.review_count
      product.score2 = (tmpS2*tmp + decimal.Decimal(request.POST['score2']))/product.review_count
      product.score3 = (tmpS3*tmp + decimal.Decimal(request.POST['score3']))/product.review_count
      product.score4 = (tmpS4*tmp + decimal.Decimal(request.POST['score4']))/product.review_count
      product.save()

    key = SECRET['API_SECRET']
    product_id = str(pID)
    url = 'http://www.kopis.or.kr/openApi/restful/pblprfr/'+product_id+'?service='+key
    req = requests.get(url).text
    xmlObject = xmltodict.parse(req)
    p_data = xmlObject['dbs']['db']

    sort = request.GET.get('detail_sort','')
    img_url = p_data['styurls']['styurl']
    if len(img_url) >=10:
          d_img = img_url
    elif len(img_url) >=3:
      if sort == 'detail2':
          d_img = img_url[1]
      elif sort == 'detail3':
          d_img = img_url[2]
      else :
          d_img = img_url[0]
          
    ctx = {
      'product':product,
      'product_api':p_data,
      'd_img':d_img,
    }
    return render(request, 'musical_detail.html', ctx)

def like_product(request, pID):
      product = Product.objects.get(pID=pID)
      product.likes.add(request.user)
      product.save()
      return redirect('musical', product.pID)

def detail(request, id):
    post_detail = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post = post_detail)


    # 조회수 기능
    tmp_view_count = post_detail.view_count
    post_detail.view_count = tmp_view_count + 1
    if post_detail.view_count >= 30:
          post_detail.is_liked = True
    post_detail.save()

    # 댓글 기능
    if request.method == 'POST':
      new_comment = Comment()
      new_comment.post = post_detail
      new_comment.writer = request.user
      new_comment.contents = request.POST['contents']
      new_comment.save()

    tags = post_detail.tags.all().values()
    if len(tags)==0:
          tag = tags
    else:
          tag = tags[0]['title']
    ctx = {
      'post':post_detail,
      'comments':comments,
      'tag':tag
    }
    return render(request, 'detail.html', ctx)

def post_scrap(request, id):
      post = Post.objects.get(id=id)
      post.scrap.add(request.user)
      post.save()
      return redirect('musical', post.id)

def community(request):
    sort = request.GET.get('sort','')
    if sort == 'likes':
          posting = Post.objects.filter(is_liked=True).order_by('-created_date')
    elif sort == 'review':
          posting = Post.objects.filter(is_review=True).order_by('-created_date')
    else :
          posting = Post.objects.all().order_by('-created_date')
    
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw','') #검색어

    if kw:
          posting = posting.filter(
            Q(title__icontains=kw) |
            Q(text__icontains=kw) 
          ).distinct()
    
    #페이징처리
    paginator = Paginator(posting, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    ctx = {'posting': page_obj, 'page': page, 'kw': kw}
    return render(request, 'community.html', ctx)

def mypage(request):
    user = request.user
    mypost = user.writer_post.filter(is_review=False).order_by('-created_date')
    myreview = user.writer_post.filter(is_review=True).order_by('-created_date')
    myscrap = user.liked_post.all()
    myproduct = user.liked_product.all()
    ctx = {
      'user':user,
      'mypost':mypost,
      'myreview':myreview,
      'myscrap':myscrap,
      'myproduct':myproduct,
    }
    return render(request, 'mypage.html', ctx)


def create(request):
    if request.method == 'GET':
      return render(request, 'create.html')

    elif request.method == 'POST':
      new_post = Post()
      new_post.title = request.POST['title']
      new_post.category = request.POST['category']
      new_post.text = request.POST['text']
      new_post.writer = request.user
      # new_post.tags = request.POST['tags']
      # 이미지 입력 받을까요 말까요
      # new_post.img = request.POST['img']
      new_post.save()

      tag_name = request.POST['tags']
      if tag_name:
        if Product.objects.filter(title=tag_name) :
          product_tag = Product.objects.get(title=tag_name)
          new_post.tags.add(product_tag)
          new_post.save()

      if new_post.category == 'review':
        new_post.is_review = True
        new_post.save()

      return redirect('detail', new_post.id)

@login_required(login_url='login')
def modify(request, id):
  post = get_object_or_404(Post, pk=id)
  if request.user != post.writer:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('detail', id=id)
  if request.method == "GET":
        post = get_object_or_404(Post, pk=id)
        return render(request, 'modify.html', {'post': post})
  if request.method == 'POST':
    post.writer = request.user
    title = request.POST['title']
    text = request.POST['text']
    category = request.POST['category']

    post.title = title
    post.text = text
    post.category = category
    post.save()
    return redirect('detail', id=id)
      
@login_required(login_url='login')
def delete(request, id):
  post = get_object_or_404(Post, pk=id)
  if request.user != post.writer:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('detail', id=id)
  post.delete()
  return redirect('community')

