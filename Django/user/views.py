from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Hit_and_Blow_View(TemplateView):
    template_name = "user/index.html"
class Sign_in_View(TemplateView):
    template_name = "user/index_sign.html"

class Calculate_View(TemplateView):
    template_name = "user/index_cal.html"

class Bmi_View(TemplateView):
    template_name = "user/index_bmi.html"