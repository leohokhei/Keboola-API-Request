#################################################################################################
### Keboola API Request                                                                       ###
### Prepared by Leo Chan                                                                      ###
### Python Ver 2.7                                                                            ###
### Requirements:                                                                             ###
### API request and output into CSV                                                           ###
### Details:                                                                                  ###
### 1. This program will output all the answers but the forms which are not completed.        ###
### 2. This program can output up to as many forms it is available with the given API.        ###
### 3. NaN are used for responses that are missing.                                           ###
#################################################################################################
 
import requests
import csv
import json
########################################
### request forms from the given API ###
########################################
forms = requests.get("http://api.typeform.com/v1/forms?key=ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d")
print "Server status: " + str(forms.status_code)

forms_json = json.loads(forms.text)
#print forms_json[0]["id"]

if forms.status_code!=200:
    print "Service is not available at the moment"

###############################################
### find out how many forms are in the list ###
forms_length=len(forms_json)

####################################################
### break down the URL to access different forms ###
#print forms_length
url_1 = "https://api.typeform.com/v1/form/"
url_2 = "?key=ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d"

##################################
### access the source by forms ###
itr = 0
while(itr<forms_length):
    full_url = str(url_1+forms_json[itr]["id"]+url_2)

    ##############################################################
    ### creating an excel sheet with the name of the form name ###
    data_csv = open( str(forms_json[itr]['name'])+'.csv','w')
    csvwriter = csv.writer(data_csv)
#    print str(forms_json[itr]['name'])+'.csv'

    #################################
    ### request data for the form ###
    data = requests.get(full_url)
    print "Form status: " + str(data.status_code)
    data_json = json.loads(data.text)

    #######################################
    ### verify if the form is completed ###
    all_entry = len(data_json['responses'])
    entries = 0
    ### First, output the header to the CSV using every questions' ID ###
    header = []
    count = 0
    questions = len(data_json['questions'])
    while(count<questions):
        header.append(str(data_json['questions'][count]['id']))
        count+=1
    csvwriter.writerow(header)


    #############################
    ### Outputing the answers ###
    #############################   
    while(entries<all_entry):

        ############################################
        ### Not outputing if form is Incompleted ###
        if(int(data_json['responses'][entries]['completed'])==0):
            entries+=1

        ###################################
        ### Output if form is completed ###
        else:
            ## create empty list ##
            values = []
            values_count=0
            while values_count<questions:
                values.append('NaN')
                values_count+=1

            answers_count = 0
            path = data_json['responses'][entries]['answers']
            ### Search to see if there are answers for the questions and Input answers into the list ###
            while(answers_count < questions):
                try:
                    values[answers_count]=str(path[header[answers_count]])
                    answers_count+=1
                ### if the ID does not exist in the answers ###
                except KeyError:
                    answers_count+=1
     
            csvwriter.writerow(values)
            entries+=1
        
    ### close the excel file ###
    data_csv.close()
    itr+=1
    #######################################################
    ### break the while loop if there are no more forms ###
    #######################################################
    if (itr==forms_length):
        break
