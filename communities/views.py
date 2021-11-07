#####################################
# dj default imports
#####################################
from django.contrib.auth.decorators import login_required

#####################################
# HTML routing imports
#####################################
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

#####################################
# Messages
#####################################
from django.contrib import messages

from users.models import CustomUser

#####################################
# Necessary models
#####################################

from .models import Post,Comment

#####################################
# Necessary forms
#####################################
from .forms import PostForm, CommentForm
#####################################
# Outside imports
#####################################
from django.utils import timezone

@login_required
def viewIndex(request):
	# order the posts
	listModelPosts = Post.objects.all().order_by('-pub_date')

	context = {
		"listModelPosts":listModelPosts,
	}
	return render(request,'communities/index.html',context = context)

@login_required
def viewCreatePost(request):
	modelPost = Post()

	formPostForm = PostForm(instance=modelPost)

	if request.method == "POST":

		# fill with post data
		formPostForm = PostForm(request.POST)

		modelCreatedPost = formPostForm.save(commit=False)

		formPostForm = PostForm(request.POST)

		if formPostForm.is_valid():
			# save the object
			user = request.user

			modelCreatedPost.author = user

			modelCreatedPost.save()

			# show message that post created
			messages.success(request, "Post created.")

			# redirect
			return redirect('communities:index')
	
	context = {
		"formPostForm":formPostForm,
	}
	return render(request, 'communities/create_post.html',context)

@login_required
def viewLikePost(request,post_id):
	modelPost = get_object_or_404(Post,id=post_id)

	if(modelPost.user_likes.filter(id=request.user.id).exists()):
		modelPost.user_likes.remove(request.user)
	else:
		modelPost.user_likes.add(request.user)
	
	return redirect('communities:index')

@login_required
def viewPostDetail(request, slug,username):
	modelPostAuthor = get_object_or_404(CustomUser, username=username)
	modelPost = get_object_or_404(Post,slug=slug,author=modelPostAuthor)

	listmodelComments = modelPost.comments.all

	context = {
		"modelPost":modelPost,
		"listmodelComments":listmodelComments,
	}
	return render(request, 'communities/post_detail.html',context)

@login_required
def viewProfile(request, username):
	modelUser = get_object_or_404(CustomUser, username = username)

	context = {
		"strUsername":modelUser.username,
		"intUsersHelped":modelUser.int_users_helped,
		"intDaysActive":modelUser.int_days_active,
		"strDateJoined":modelUser.date_joined,
		"strAbout":modelUser.text_about,
	}

	return render(request, "communities/profile.html",context)

############
# Creating comments
# With reference to:
# https://stackoverflow.com/questions/44837733/how-to-make-add-replies-to-comments-in-django
############
@login_required
def viewCreateComment(request,username,slug):
	# get the author
	modelPostAuthor = get_object_or_404(CustomUser,username = username)
	# get the post
	modelPost = get_object_or_404(Post, slug = slug,author = modelPostAuthor)

	# get list of active parent comments
	listComments = modelPost.comments.filter(active = True, parent__isnull=True)


	if request.method == "POST":
		print("asdfasdfasd")
		# get the current user
		modelUser = request.user

		# form for comment
		formCommentForm = CommentForm(data=request.POST)

		if formCommentForm.is_valid():

			modelParentObj = None
			# try to get parent comment id from hidden input
			try:
				intParentId = int(request.POST.get("intParentId"))
			except:
				intParentId = None
			# if parent has been submitted get the parent's id
			if intParentId:
				modelParentObj = Comment.objects.get(id=intParentId)
				# if there exists a parent
				if modelParentObj:
					# create reply
					modelReplyComment = formCommentForm.save(commit=False)
					# put user with comment
					modelReplyComment.author = modelUser
					# put the parent id in the reply
					modelReplyComment.parent = modelParentObj
			# Else, this is a normal comment
			# create but dont save to db
			modelNewComment = formCommentForm.save(commit = False)
			modelNewComment.post = modelPost
			modelNewComment.author = modelUser

			# save
			modelNewComment.save()
			messages.success(request, "Comment created.")
			return redirect('communities:index')

	else:
		formCommentForm = CommentForm()

	context = {
		"formCommentForm":formCommentForm,
		"listComments":listComments,
		"modelPost":modelPost,
	}


	return render(request,'communities/create_comment.html',context=context)

