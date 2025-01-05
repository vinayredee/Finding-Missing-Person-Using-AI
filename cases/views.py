from django.shortcuts import render, redirect
from .forms import MissingPersonForm

def add_case(request):
    # Handle the form submission when the request method is POST
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)  # Handle POST data and file upload
        if form.is_valid():
            form.save()  # Save the valid form data to the database
            return redirect('cases:add_case')  # Redirect to the "find_person" page after successful form submission
    else:
        form = MissingPersonForm()  # Create an empty form for GET requests

    return render(request, 'cases/add_case.html', {'form': form})  # Render the form on the page