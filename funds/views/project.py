from django.db.models import Sum, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from funds.forms import ProjectForm, ProjectPictureForm
from funds.models.comment import Comment
from funds.models.project import Project
from funds.models.projectPicture import ProjectPicture
from funds.models.rating import Rating
from funds.models.donation import Donation


# TODO Find a way to give the user an option to add another image on demand & not restrict him to a no.
@login_required
def create(request):
    ProjectPictureFormSet = modelformset_factory(ProjectPicture, form=ProjectPictureForm, extra=1, max_num=3)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST or None)
        formset = ProjectPictureFormSet(request.POST or None, request.FILES or None,
                                        queryset=ProjectPicture.objects.none())

        if project_form.is_valid() and formset.is_valid():
            project_instance = project_form.save(commit=False)
            project_instance.user = request.user
            project_instance.save()

            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    project_picture_object = ProjectPicture(project=project_instance, image=image)
                    project_picture_object.save()
                except Exception as e:
                    break

            return redirect('myprojects')
    else:
        project_form = ProjectForm()
        formset = ProjectPictureFormSet(queryset=ProjectPicture.objects.none())
    return render(request, 'funds/add.html',
                  {'project_form': project_form, 'formset': formset})


# * This function including it's html is just for testing
@login_required
def show_all(request):
    all_projects = Project.objects.filter(user=request.user)
    return render(request, 'funds/myprojects.html', {'projects': all_projects})


# ! This method gives out an error: render() got an unexpected keyword argument 'renderer' & I am still investigating
# @login_required
# def create(request):
#     if request.method == "POST":
#         project_form = ProjectForm(request.POST)
#         if project_form.is_valid():
#             project_instance = project_form.save(commit=False)
#             project_instance.user = request.user
#             project_instance.save()
#             return redirect('myprojects')
#     else:
#         project_form = ProjectForm()
#         return render(request, 'funds/add.html', {'form': project_form}, renderer=None)

#TODO 1- Add Ajax for comments and reports
#TODO 2- Adding the ability for the user to insert his own tags in funds/templates/funds/add.html
#TODO 3- We need to make the add.html form look much better
#TODO 4- Adding slider of the project gallery in project_read.html
#TODO 5- Users can rate the projects
#TODO 6- Project creator can cancel the project if the donations are less than 25% of the target.
#TODO 7- Project page should show the overall average rating of the project + the number of the raters
#TODO 8- Project page should show 4 other similar projects based on project tags.

@login_required
def read(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    ratings = Rating.objects.filter(project=project).aggregate(Avg('rating'))
    if ratings['rating__avg'] == None :
        ratings['rating__avg'] = 0.0

    images = ProjectPicture.objects.filter(project=project)
    comments = Comment.objects.filter(project=project)
    donations = Donation.objects.filter(project=project).aggregate(Sum('donation'))
    if donations['donation__sum'] == None :
        donations['donation__sum'] = 0

    total_target = project.total_target
    total_target_percent = round((donations['donation__sum'] / total_target) * 100, 1)

    context = {'project_data': project,
            'project_images': images,
            'project_ratings': ratings,
            'project_donations': donations,
            'project_comments': comments,
            'project_target_percent': total_target_percent}

    

    if request.method == 'POST':

        if request.POST.__contains__('comment'):
            comment_body = request.POST.get('comment')
            user = request.user
            comment = Comment.objects.create(comment=comment_body,user=user,project=project)
            
        
        if request.POST.__contains__('comment-report'):
            print(request.POST) 
            print("done!!!!!!!!!!!!!!!")
            print(request.POST.get('comment-report')) 
        
        return redirect('project_read', project_id=project_id)


    else:
    # render template to display the data
        return render(request, 'funds/read_project.html', context)


    # else:
    # # query to get data about specific item
    #     project = get_object_or_404(Project, id=project_id)
    #     ratings = Rating.objects.filter(project=project).aggregate(Avg('rating'))
    #     images = ProjectPicture.objects.filter(project=project)
    #     comments = Comment.objects.filter(project=project)
    #     donations = Donation.objects.filter(project=project).aggregate(Sum('donation'))
    #     total_target = project.total_target
    #     total_target_percent = round((donations['donation__sum'] / total_target) * 100, 1)

    #     context = {'project_data': project,
    #             'project_images': images,
    #             'project_ratings': ratings,
    #             'project_donations': donations,
    #             'project_comments': comments,
    #             'project_target_percent': total_target_percent}

    #     # render template to display the data
    #     return render(request, 'funds/read_project.html', context)

