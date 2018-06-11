from django.shortcuts import (
    get_object_or_404,
    HttpResponse,
    render,
)

from .decorators import statistics
from .forms import ImageForm
from .models import ImageUploader


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.POST['name']
            try:  # check if image already exists
                previous_image = ImageUploader.objects.get(pk=filename)
            except ImageUploader.DoesNotExist:
                image_file = ImageUploader(image=request.FILES['image'],
                                           filename=filename)
                image_file.save()
                msg = 'uploaded'
            else:
                previous_image.image.delete()
                previous_image.image = request.FILES['image']
                previous_image.save()
                msg = 'changed'
            return HttpResponse("{0} image {1}!".format(filename, msg))
    else:
        form = ImageForm()
    return render(request, 'uploader/upload_image.html', {'form': form})


# @statistics
def show_image(request, image_name):
    image = get_object_or_404(ImageUploader, pk=image_name)
    return render(request,
                  'uploader/show_image.html',
                  {'image_name': image_name, 'image': image})
