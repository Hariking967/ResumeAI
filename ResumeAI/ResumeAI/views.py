from django.shortcuts import redirect, render

def home(request):
    if request.method == 'POST':
        form = DocTextForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DocTextForm()
    return render(request, 'home.html',{'form':form})