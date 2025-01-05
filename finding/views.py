from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageUploadForm
from cases.models import MissingPerson
import face_recognition
import os
import logging
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)

def find_person(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            # Replace spaces in the uploaded image name
            uploaded_image_name = uploaded_image.name.replace(" ", "_")
            uploaded_image_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_photos', uploaded_image_name)

            # Save the uploaded image
            os.makedirs(os.path.dirname(uploaded_image_path), exist_ok=True)  # Ensure directory exists
            with open(uploaded_image_path, 'wb') as f:
                for chunk in uploaded_image.chunks():
                    f.write(chunk)

            try:
                # Convert the uploaded image to face encoding
                uploaded_image_data = face_recognition.load_image_file(uploaded_image_path)
                uploaded_encodings = face_recognition.face_encodings(uploaded_image_data)

                if uploaded_encodings:
                    uploaded_encoding = uploaded_encodings[0]  # Use the first face found
                    missing_people = MissingPerson.objects.all()

                    best_match = None

                    for person in missing_people:
                        try:
                            # Ensure the directory exists and load the missing person's image
                            if not os.path.exists(person.photo.path):
                                logger.warning(f"Image for {person.name} not found at {person.photo.path}")
                                continue  # Skip if the image is missing

                            known_image_data = face_recognition.load_image_file(person.photo.path)
                            known_encodings = face_recognition.face_encodings(known_image_data)

                            if known_encodings:
                                known_encoding = known_encodings[0]  # Use the first face found

                                # Compare the face encodings
                                results = face_recognition.compare_faces([known_encoding], uploaded_encoding)

                                # If a match is found, set this as the best match
                                if results[0]:
                                    best_match = person
                                    break  # No need to continue searching once a match is found
                                
                        except Exception as e:
                            logger.error(f"Error processing image for {person.name}: {e}")
                            continue  # Skip to the next person if there's an error

                    if best_match:
                        # If a match is found, render the result page with the person's info and photo
                        uploaded_image_url = f"{settings.MEDIA_URL}uploaded_photos/{uploaded_image_name}"  # Pass uploaded image URL
                        return render(request, 'finding/result.html', {
                            'person': best_match,
                            'image_url': best_match.photo.url,  # Missing person's photo
                            'uploaded_image_url': uploaded_image_url,  # Uploaded photo
                        })
                    return render(request, 'finding/not_found.html')

            except Exception as e:
                logger.error(f"Error processing uploaded image: {e}")
                # Handle the error (e.g., render an error page or return a message)

    else:
        form = ImageUploadForm()  # Create a new form instance for GET requests

    return render(request, 'finding/find_person.html', {'form': form})  # Render the upload page




