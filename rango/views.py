from django.shortcuts import render
from models import Category,Page
def index(request):
	cat = Category.objects.order_by('-likes')[:5]
	context = {'cat_list':cat}
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


