from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.
class Hit_and_Blow_View(TemplateView):
    template_name = "user/index_game.html"

    def post(self, request):
        if request.method == "POST":
            if "code" not in request.body.decode():
                player_name = request.POST.get('player_name')
                hidden_num = request.POST.get('hidden_num')
                cpu_level = request.POST.get('cpu_level')

                params = {
                    'player_name': player_name,
                    'hidden_num': hidden_num,
                    'cpu_level': cpu_level,
                }
                return render(request, 'user/index_game.html', params)
            else:
                guess = request.POST.get('code')
                player_name = request.POST.get('h_player_name')
                hidden_num = request.POST.get('h_hidden_num')
                cpu_level = request.POST.get('h_cpu_level')
                params = {
                    'guess' : guess,
                    'player_name': player_name,
                    'hidden_num': hidden_num,
                    'cpu_level': cpu_level,
                }
                return render(request, 'user/index_game.html', params)

class Sign_in_View(TemplateView):  
    template_name = "user/index_sign.html"

class Game_Over(TemplateView):  
    template_name = "user/index_over.html"
class Calculate_View(TemplateView):
    template_name = "user/index_cal.html"
class Bmi_View(TemplateView):
    template_name = "user/index_bmi.html"

