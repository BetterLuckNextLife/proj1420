from django.shortcuts import render
import imageGenerator
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'index.html', {})
    if request.method == "POST":
        if "linker" in request.POST:
            addr = request.POST.get("linker")
            imageGenerator.gen_image(addr=addr)
            return redirect('/')