from django.db.models import Sum, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from taggit.models import Tag
from django.contrib import messages
import datetime

from funds.forms import ProjectForm, ProjectPictureForm
from funds.models.comment import Comment
from funds.models.project import Project
from funds.models.projectPicture import ProjectPicture
from funds.models.rating import Rating
from funds.models.donation import Donation
from funds.models.commentReport import CommentReport
from funds.models.projectReport import ProjectReport


@login_required
def create(request):
    ProjectPictureFormSet = modelformset_factory(
        ProjectPicture, form=ProjectPictureForm, extra=1, max_num=10)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST or None)
        formset = ProjectPictureFormSet(request.POST or None, request.FILES or None, queryset=ProjectPicture.objects.none())

        # Checking if form is valid
        title = request.POST['title']
        details = request.POST['details']
        category = request.POST['category']
        tags = request.POST['tags']
        total_target = request.POST['total_target']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if not title or not details or not category or not tags or not total_target or not start_date or not end_date:
            messages.error(request, "No field can be empty!")
            return redirect("project_add")
        if datetime.datetime.strptime(start_date, "%Y-%m-%d").ctime() >= datetime.datetime.strptime(end_date, "%Y-%m-%d").ctime():
            messages.error(request, "Invalid start and end date!")
            return redirect("project_add")
        if int(total_target) < 1:
            messages.error(request, "Invalid target!")
            return redirect("project_add")
        if len(request.FILES) == 0:  # No images entered
            messages.error(request, "A project must contain at least one image!")
            return redirect("project_add")


        if project_form.is_valid() and formset.is_valid():
            project_instance = project_form.save(commit=False)
            project_instance.user = request.user
            project_instance.save()
            # Without this next line the tags won't be saved.
            project_form.save_m2m()
            # project_instance.tags.set(project_form.cleaned_data['tags'])

            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    project_picture_object = ProjectPicture(project=project_instance, image=image)
                    project_picture_object.save()
                except Exception as e:
                    break

            return redirect('project_read', project_id=project_instance.id)
    else:
        project_form = ProjectForm()
        formset = ProjectPictureFormSet(queryset=ProjectPicture.objects.none())
    return render(request, 'funds/add.html', {'project_form': project_form, 'formset': formset})


# * This function including it's html is just for testing
@login_required
def show_all(request):
    all_projects = Project.objects.filter(user=request.user)
    return render(request, 'funds/myprojects.html', {'projects': all_projects})


@login_required
def delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('myprojects')


@login_required
def read(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    ratings_query = Rating.objects.filter(project=project).aggregate(Avg('rating'))
    if ratings_query['rating__avg'] == None:
        ratings_query['rating__avg'] = 0.0

    ratings = round(ratings_query['rating__avg'], 2)
    ratings_count = Rating.objects.filter(project=project).aggregate(Count('rating'))
    ratings_count_user = Rating.objects.filter(project=project, user=request.user).aggregate(Count('rating'))
    ratings_count_user_final = ratings_count_user['rating__count']

    images = ProjectPicture.objects.filter(project=project)
    comments = Comment.objects.filter(project=project)
    donations = Donation.objects.filter(project=project).aggregate(Sum('donation'))
    if donations['donation__sum'] == None:
        donations['donation__sum'] = 0

    total_target = project.total_target
    total_target_percent = round(
        (donations['donation__sum'] / total_target) * 100, 2)

    similar_projects = Project.objects.filter(tags__in=Project.objects.filter(pk=project_id).values_list('tags')).exclude(pk=project_id).all().distinct()[:4]

    context = {'project_data': project,
               'project_images': images,
               'project_ratings': ratings,
               'project_ratings_count': ratings_count,
               'project_ratings_count_per_user': ratings_count_user_final,
               'project_donations': donations,
               'project_comments': comments,
               'project_target_percent': total_target_percent,
               'similar_projects': similar_projects,
               'session_user': request.user}

    if request.method == 'POST':

        if request.POST.__contains__('comment'):
            comment_body = request.POST.get('comment')
            user = request.user
            comment = Comment.objects.create(comment=comment_body, user=user, project=project)

        if request.POST.__contains__('comment-report'):
            report_body = request.POST.get('comment-report')
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            user = request.user
            commentReport = CommentReport.objects.create(report=report_body, user=user, comment=comment)

        if request.POST.__contains__('project-report'):
            project_report_body = request.POST.get('project-report')
            user = request.user
            projectReport = ProjectReport.objects.create(report=project_report_body, user=user, project=project)

        if request.POST.__contains__('donation'):
            donation_num = request.POST.get('donation')
            user = request.user
            donation = Donation.objects.create(donation=donation_num, user=user, project=project)

        if request.POST.__contains__('rating-form'):
            rate = request.POST.get('rating-form')
            user = request.user
            ratingObj = Rating.objects.create(rating=rate, user=user, project=project)

        if request.POST.__contains__('edit-rating-form'):
            user = request.user
            rate = request.POST.get('edit-rating-form')
            ratingObj = Rating.objects.filter(user=user, project=project).first()
            ratingObj.rating = rate
            ratingObj.save()

        return redirect('project_read', project_id=project_id)

    else:
        # render template to display the data
        return render(request, 'funds/read_project.html', context)


def tagged(request):
    tag = get_object_or_404(Tag)
    # Filter posts by tag name
    projects = Project.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': projects,
    }
    return render(request, 'home.html', context)
