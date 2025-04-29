from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json


@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    success_url = reverse_lazy('home-page')
    template_name = 'home.html'

class Typography(ListView):
    model = Organization
    content_object_name = 'typography'
    success_url = reverse_lazy('typography-list')


# Organization
class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'organization/del.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationList(ListView):
    model = Organization
    template_name = 'organization/list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name_icontains=query) | Q(description_icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/add.html'
    success_url = reverse_lazy('organization-list')


# OrgMember

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember/del.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember/edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'object_list'  # Changed from 'orgmember' to match template
    template_name = 'orgmember/list.html'
    paginate_by = 5

    def get_queryset(self):
        return OrgMember.objects.select_related('student', 'organization')

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember/add.html'
    success_url = reverse_lazy('orgmember-list')


# Student
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student/del.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/edit.html'
    success_url = reverse_lazy('student-list')

class StudentList(ListView):
    model = Student
    template_name = 'student/list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = Student.objects.select_related('program')
        if self.request.GET.get("q"):
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(student_id__icontains=query) |
                Q(lastname__icontains=query) |
                Q(firstname__icontains=query)
            )
        return qs


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/add.html'
    success_url = reverse_lazy('student-list')

def student_list(request):
    students = Student.objects.all()
    print("Students fetched:", students) 
    return render(request, "student/list.html", {"object_list": students})

# College

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college/del.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college/edit.html'
    success_url = reverse_lazy('college-list')

class CollegeList(ListView):
    model = College
    template_name = 'college/list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = College.objects.all()
        if self.request.GET.get("q"):
            query = self.request.GET.get('q')
            qs = qs.filter(college_name__icontains=query)
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college/add.html'
    success_url = reverse_lazy('college-list')



# Program

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program/del.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/edit.html'
    success_url = reverse_lazy('program-list')

class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program/list.html'
    paginate_by = 5

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/add.html'
    success_url = reverse_lazy('program-list')


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Organizations by College
        org_college_data = Organization.objects.values('college__college_name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context['college_labels'] = json.dumps([item['college__college_name'] for item in org_college_data])
        context['org_by_college'] = [item['count'] for item in org_college_data]

        # Students by Program
        student_program_data = Student.objects.values('program__prog_name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context['program_labels'] = json.dumps([item['program__prog_name'] for item in student_program_data])
        context['students_by_program'] = [item['count'] for item in student_program_data]

        # Member Growth over time
        member_growth = OrgMember.objects.annotate(
            month=TruncMonth('date_joined')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        context['months_labels'] = json.dumps([item['month'].strftime('%b %Y') for item in member_growth])
        context['member_growth'] = [item['count'] for item in member_growth]

        # Organization Distribution
        org_distribution = Organization.objects.annotate(
            member_count=Count('orgmember')
        ).order_by('-member_count')

        context['org_names'] = json.dumps([org.name for org in org_distribution])
        context['org_members'] = [org.member_count for org in org_distribution]

        return context