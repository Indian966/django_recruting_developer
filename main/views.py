from django.shortcuts import render, redirect
from main.models import User, Post, Company, Application

import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

class PostView(View) :

    # 채용 공고 불러오기 && 검색
    def get(self, request):
        try:
            search = request.GET.get('search', None)

            q = Q()

            if search:
                q &= Q(company__name__icontains=search)
                q &= Q(position__icontains=search)
                q &= Q(content__icontains=search)
                q &= Q(tech__icontains=search)

            results = [{
                'id': post.id,
                'company': post.company.name,
                'region': post.company.region,
                'reward': post.reward,
                'position' : post.position,
                'content': post.content,
                'tech': post.tech,
            } for post in Post.objects.filter(q).distinct()]
            return render(request, "index.html", {'post_list' : results})

        except KeyError:
            return JsonResponse({"message": "Key Error"}, status=400)


class PostDetailView(View) :
    # 채용 상세 정보
    def get(self, request, post_id):
        print("GET")
        if not Post.objects.filter(id=post_id).exists() :
            return JsonResponse({'GET message' : 'No post'}, status=404)

        post = Post.objects.get(id=post_id)
        result = {
            'post_id': post.id,
            'company': post.company.name,
            'position': post.position,
            'reward': post.reward,
            'content': post.content,
            'tech': post.tech
        }
        return render(request, "post_view.html", {'post_info' : result})

    # 채용 공고 수정
    def post(self, request, post_id):
        print("POST")
        try :
            position = request.POST['position']
            reward = request.POST['reward']
            content = request.POST['content']
            tech = request.POST['tech']

            post = Post.objects.get(id=post_id)

            post.position = position
            post.reward = reward
            post.content = content
            post.tech = tech

            post.save()

            return redirect('/')
        except :
            return JsonResponse({'PUT message': 'No post'}, status=401)

    def temp(self, request):
        if request.method == delete:
            print("yee")



class NewPostView(View) :
    # 채용 공고 등록
    def post(self, request):
        try:
            print("request : ",request.POST)
            # print(request.body)
            # data = json.loads(request.POST)

            company = request.POST['id']
            position = request.POST['position']
            reward = request.POST['reward']
            content = request.POST['content']
            tech = request.POST['tech']

            Post.objects.create(
                company_id=company,
                position=position,
                reward=reward,
                content=content,
                tech=tech
            )
            return redirect('/')

        except KeyError:
            return JsonResponse({'message': 'Key Error'}, status=400)

    def get(self, request):
        # 뷰 로직 작성
        return render(request, "new-post.html")

class ApplicationView(View):
    # 채용공고에 지원하기
    def post(self, request, recruiting_id, user_id):
        if not Application.objects.filter(user__id=user_id).exists():
            return JsonResponse({'message' : '이미 지원한 공고'}, status=404)
        try:
            data = json.loads(request.body)

            post = data['post_id']
            user = data['user_id']

            Application.objects.create(
                post = post,
                user = user,
            )
            return JsonResponse({'message' : '지원 완료'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'Key Error'}, status=400)


# # Create your views here.
# def index(request):
#     post_list = Post.objects.all()
#     return render(request, "index.html", {'post_list' : post_list}) # index.html 렌더링
#
# def new_post(request):
#     # Cop()
#     if request.method == 'POST':
#         new_article = Post.objects.create(
#             cop_id=request.POST['cop_id'],
#             position = request.POST['position'],
#             money = request.POST['money'],
#             content = request.POST['content'],
#             tech = request.POST['tech']
#         )
#         return redirect('index')
#
#     return render(request, "new-post.html") # greet.html 렌더링


# 채용 공고 삭제
    def delete(self, request, post_id):
        print('delete')
        if not post.objects.filter(id=post_id).exists():
            return JsonResponse({'message': '없는 채용공고입니다'}, status=404)
        post = post.objects.get(id=post_id)
        post.delete()

        return redirect('/')