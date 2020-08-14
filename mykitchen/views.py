from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mykitchen/mykitchen_index.template.html', {
    })