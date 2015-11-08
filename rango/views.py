from django.shortcuts import render
from models import Category,Page
from forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	cat = Category.objects.order_by('-likes')[:5]
	page = Page.objects.order_by('-views')[:5]
	context = {'cat_list':cat,'pages':page}
	return render(request,'index.html',context)

def category(request,category_name_url):
	context = {}
	try:
		category = Category.objects.get(slug=category_name_url)
		context['category']=category
		pages		 = Page.objects.filter(Category=category)
		context['pages']=pages
	except:
		pass	
	return render(request,'category.html',context)

@login_required
def add_category(request):
	if request.method == 'POST':
		form	=	CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form	=	CategoryForm()

		return render(request,'add_category.html',{'form':form})				

@login_required
def add_page(request,category_name_url):
	try:
		cat = Category.objects.get(slug=category_name_url)
	except Category.DoesNotExist:
		cat = None	
	if request.method == 'POST':
		form	=	PageForm(request.POST)

		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.Category = cat
				page.views = 0
				page.save()
			return category(request,category_name_url)
		else:
			print form.errors
	else:
		form	=	PageForm()

		return render(request,'add_page.html',{'form':form})

def register(request):
	registered	=	False
	if request.method=='POST':
		userform = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if userform.is_valid() and profile_form.is_valid():
			user = userform.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile['picture'] = request.FILES['picture']

			profile.save()
			registered = True

		else:
			print userform.errors, profile_form.errors
	else:
		userform = UserForm()
		profile_form = UserProfileForm()


	return render(request,'register.html',{'userform':userform,'profileform':profile_form,'reg_status':registered})

def user_login(request):
	if request.method == 'POST':
		username	=	request.POST.get('username')
		password	=	request.POST.get('password')

		user = authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse('User not activated')
		else:
			return HttpResponse('username or password incorrect')
	else:
		return render(request,'login.html',{})

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/rango/')									



