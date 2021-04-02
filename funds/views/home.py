from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funds.models.project import Project
from funds.models.rating import Rating
from funds.models.projectPicture import ProjectPicture
from funds.models.category import Category
from django.db.models import Sum
from django.db.models import Max


def get_all_data():
    projects_with_rating = Project.objects.all()
    project_list = []
    category_list = Category.objects.all()
    print(projects_with_rating)
    for p in projects_with_rating:
        rate = Rating.objects.filter(project=p).aggregate(Sum('rating'))
        if rate['rating__sum'] == None:
            rate['rating__sum'] = 0
        if ProjectPicture.objects.filter(project=p):
            img = ProjectPicture.objects.filter(project=p)[0]
        else:
            img = None
        print("=========================")
        print(img)
        print("=========================")
        dict = {
            'project': p,
            'rate': rate['rating__sum'],
            'img': img
        }
        project_list.append(dict)
    top_projects = sorted(project_list, key=lambda i: i['rate'], reverse=True)[:5]
    print("HERE NEW LIST OF 5 :  ")
    print(top_projects)
    context = {
        'top_projects': top_projects,
        'all_projects': project_list,
        'category': category_list,
        'Projects_by_category': None,
    }
    return context


@login_required
def index(request):
    if request.method == 'POST':
        category_id = request.POST.get("category", None)
        if category_id:
            Projects_by_category = Project.objects.prefetch_related('category').filter(category=category_id)
            print(Projects_by_category)
            context = get_all_data()
            context['Projects_by_category'] = Projects_by_category
            return render(request, 'funds/home.html', context)
    else:
        context = get_all_data()
        return render(request, 'funds/home.html', context)


def search(request):
    return render(request, 'funds/search.html')
