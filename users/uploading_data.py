from users.models import Afiliado, Period
import csv
import os
import mimetypes
from django.http.response import HttpResponse
from django.utils import timezone


STATE_GOOD = 'G'
STATE_BAD = 'B'
STATE_PROCESS = 'P'

NUM_DOCUMENT = 0
VALIDATION_ONE = 1
VALIDATION_TWO = 2
VALIDATION_THREE = 3
STATE_POS = 4

def handle_uploaded_file(f):
    # download the file of excel to my side
    with open('temp_file.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # extract and add the data to my database

    with open('temp_file.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # check first if the person already exists in the db
            # to see if we just have to modify the value
            element = Afiliado.objects.filter(document_number=int(row[NUM_DOCUMENT]))
            now = timezone.now()
            period_str = str(now.month) + "-" + str(now.year)
            if not element.exists():
                # in case the person has not been found already in the database

                person = Afiliado(document_number = int(row[NUM_DOCUMENT]), first_val = row[VALIDATION_ONE], second_val = row[VALIDATION_TWO], 
                        third_val = row[VALIDATION_THREE], state = row[STATE_POS],  date_upload = now)
                person.save()
                # add the person to the period
                per = Period(person= person, period=period_str, state=row[STATE_POS])
                per.save()

            else:
                val = Afiliado.objects.filter(document_number = int(row[NUM_DOCUMENT]))
                val.update(first_val = row[VALIDATION_ONE], second_val = row[VALIDATION_TWO], 
                        third_val = row[VALIDATION_THREE], state = row[STATE_POS],  date_upload = now)


                if not Period.objects.filter(period=period_str, person= val[0]).exists():
                    per = Period(person= val[0], period=period_str, state=row[STATE_POS])
                    per.save()
    
    # delete the temp file
    os.remove("temp_file.csv")

def download_file():
    """
    Creates a file with each of the people that are in the databse
    and lets the user download it
    """
    name = "historic_file.csv"

  
    with open(name , 'w') as destination:
        destination_writer = csv.writer(destination, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        all = Afiliado.objects.all()
        destination_writer.writerow(["Numero de Documento", "Validación Uno", "Validación Dos", "Validación Tres", "Estado Final"])
        for element in all:
            destination_writer.writerow([element.document_number, element.first_val, element.second_val, element.third_val, element.state])
        

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'historic_file.csv'
    # Define the full file path
    filepath = BASE_DIR + "/" + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

