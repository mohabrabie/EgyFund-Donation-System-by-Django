from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funds.models.project import Project
from funds.models.rating import Rating
from funds.models.projectPicture import ProjectPicture
from funds.models.category import Category
from django.db.models import Sum
from django.db.models import Max


@login_required
def index(request):
    projects_with_rating = Project.objects.all()
    project_list = []
    categoty_ist =[]
    categoty_ist = Category.objects.all()
    print(projects_with_rating)

    for p in projects_with_rating:
        rate = Rating.objects.filter(project=p).aggregate(Sum('rating'))
        if rate['rating__sum'] == None:
            rate['rating__sum'] = 0
        img = ProjectPicture.objects.filter(project=p)[0]
        dict = {
            'project': p,
            'rate': rate['rating__sum'],
            'img': img
        }
        project_list.append(dict)
    print(project_list)
    print("=======================================================")
    print(sorted(project_list, key=lambda i: i['rate'], reverse=True))
    project_list = sorted(project_list, key=lambda i: i['rate'], reverse=True)
    context = {
        'projects': project_list,
        'category': categoty_ist,
    }
    return render(request, 'funds/home.html', context)


def main(request):
    return render(request, 'funds/home.html')
