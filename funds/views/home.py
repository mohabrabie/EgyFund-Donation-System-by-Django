from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funds.models.project import Project
from funds.models.rating import Rating
from funds.models.projectPicture import ProjectPicture
from funds.models.category import Category
from django.db.models import Sum
from django.db.models import Avg


def get_all_data():
    projects_with_rating = Project.objects.all()
    project_list = []
    category_list = Category.objects.all()
    print(projects_with_rating)
    for p in projects_with_rating:
        rate = Rating.objects.filter(project=p).aggregate(Avg('rating'))
        if rate['rating__avg'] == None:
            rate['rating__avg'] = 0
        if ProjectPicture.objects.filter(project=p):
            img = ProjectPicture.objects.filter(project=p)[0]
        else:
            img = None
        dict = {
            'project': p,
            'rate': round(rate['rating__avg'], 2),
            'img': img
        }
        project_list.append(dict)
    top_projects = sorted(project_list, key=lambda i: i['rate'], reverse=True)[:5]
    first_project = top_projects[0]
    top_projects.remove(top_projects[0])
    latest_projects = sorted(project_list, key=lambda r: r['project'].start_date, reverse=True)[:5]
    project_list = sorted(project_list, key=lambda r: r['project'].start_date, reverse=True)
    print("HERE NEW LIST OF 5 :  ")
    print(latest_projects)
    context = {
        'latest_projects': latest_projects,
        'first_project': first_project,
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
        projects = Project.objects.all()
        searched = request.POST.get('searched').strip()
        if searched:
            for project in projects:
                if searched in project.tags.names() or project.title:
            # projects = Project.objects.filter(title__contains=searched)
                    return render(request, 'funds/search.html', {'searched': searched,
                                                         'projects': projects})
    else:
        context = get_all_data()
        return render(request, 'funds/home.html', context)

# def search(request):
#     if request.method == 'POST':

#     else:
#         return render(request, 'funds/search.html',{})
