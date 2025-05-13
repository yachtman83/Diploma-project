from django.shortcuts import render
from .forms import PreferenceForm
from .genetic import generate_meal_plan
from .models import Result

# Create your views here.
def input_view(request):
    result = None

    if request.method == "POST":
        form = PreferenceForm(request.POST)
        if form.is_valid():
            health_profile = form.cleaned_data['health_profile']
            goal = form.cleaned_data["calorie_goal"]
            exclude = form.cleaned_data["exclude_ingredients"].split(",")
            
            result = generate_meal_plan(health_profile, goal)

            if request.user.is_authenticated:
                Result.objects.create(
                    user=request.user,
                    result_text=str(result)
                )

            return render(request, "nutrition/results.html", {"result": result})
    else:
        form = PreferenceForm()
    return render(request, "nutrition/index.html", {"form": form})