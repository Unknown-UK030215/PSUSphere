from django.forms import ModelForm
from django import forms
from .models import Organization, OrgMember, Student, College, Program

class OrganizationForm(ModelForm):
    class meta:
        model = Organization
        fields = "__all__"

class OrgMemberForm(ModelForm):
    class meta:
        model = OrgMember
        fields = "__all__"

class StudentForm(ModelForm):
    class meta:
        model = Student
        fields = "__all__"

class CollegeForm(ModelForm):
    class meta:
        model = College
        fields = "__all__"

class ProgramForm(ModelForm):
    class meta:
        model = Program
        fields = "__all__"
