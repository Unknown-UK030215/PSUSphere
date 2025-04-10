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