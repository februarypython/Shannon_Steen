''' OOP Assignment 8: Hospital
Patient Attributes:  
    Id, Name, Allergies, Bed number(should be none by default)

Hospital Attributes:
    Patients(an empty list), Name, Capacity(integer indicating the maximum number of patients hospital can hold)

Hospital Methods:
    Admit:  Add a patient to the list of patients. 
            Assign the patient a bed number. 
            If the length of the list is >= the capacity do not admit the patient. 
            Return a message either confirming that admission is complete or saying the hospital is full.
    Discharge:  Look up and remove a patient from the list of patients. 
                Change bed number for that patient back to none. 
'''              
# Additional features outside of assignment requirements:
#     Added Display methods for both patient and hospital
#     Tied hospital to patient, so display patient reflects which hospital patient is in, if any.
#     When discharging a patient, added message to advise if said patient is not a patient of said hospital.

class Patient(object):
    patient_counter = 0
    def __init__(self, name, allergies=None, bed=None):
        self.patient_name = name
        self.allergies = allergies
        self.bed_number = None
        self.hospital_name = None
        Patient.patient_counter += 1
        self.patient_id = Patient.patient_counter
    
    def display(self):
        print "\n" + "="*30 + self.patient_name + "="*30
        print "Patient {}-{}\nAllergies: {}\nPatient at: {}\nAssigned to Bed: {}".format(self.patient_id, self.patient_name, self.allergies, self.hospital_name, self.bed_number)
        print "="*60 + "="*len(self.patient_name)
        return self

class Hospital(object):
    def __init__(self, name, capacity):
        self.hospital_name = name
        self.capacity = capacity
        self.admitted_patients = []
        # track available beds in hospital
        for i in range(1, self.capacity+1):
            self.admitted_patients.append(i)

    def display(self):
        print "\n" + "="*42 + self.hospital_name + "="*42
        if self.capacity == 0:
            print "{} Hospital is at full capacity and not accepting patients at this time.".format(self.hospital_name)
        else:
            print "{} Hospital has a max capacity of {}, and currently has {} bed(s) available.".format(self.hospital_name, len(self.admitted_patients), self.capacity)
        print "="*84 + "="*len(self.hospital_name)
        return self

    def admit(self, patient):
        if self.capacity == 0:  #hospital is full
            print "\n" + "="*30 + self.hospital_name + "="*30
            print "We're sorry, {} Hospital is at full capacity.\nWe are unable to admit {} at this time.".format(self.hospital_name, patient.patient_name)
            print "="*60 + "="*len(self.hospital_name)
        else:  #assign patient to next available bed
            for bed in range(len(self.admitted_patients)):
                if type(self.admitted_patients[bed]) == int:
                    self.capacity -= 1  #bed taken, decrement capacity
                    patient.bed_number = self.admitted_patients[bed]
                    patient.hospital_name = self.hospital_name
                    self.admitted_patients[bed] = {'name': patient.patient_name, 'allergies': patient.allergies, 'patient_id': patient.patient_id, 'bed': patient.bed_number}
                    print "\n" + "="*70
                    print "{} has now been admitted to {} Hospital.".format(patient.patient_name, self.hospital_name)
                    print "="*70
                    break  #assignment done, exit loop
        return self

    def discharge(self, patient):
        found = False
        for idx in range(len(self.admitted_patients)):
            if type(self.admitted_patients[idx]) == int: #list contains dicts of patient info and ints of available beds; if int move on
                continue
            else: #if dict, see if patient is in list of admitted patients
                for key in self.admitted_patients[idx]:
                    if self.admitted_patients[idx][key] == patient.patient_name:  #found the patient in list of admitted patients
                        self.admitted_patients[idx] = patient.bed_number  #reset bed in list to available by replacing patient info with int of bed
                        patient.bed_number = None  #reset patient bednumber to none
                        patient.hospital_name = None
                        self.capacity += 1  #bed opened, increment capacity
                        found = True
                        return self #patient released, exit
        if not found:
            print "\n" + "="*60
            print "{} is not a patient at {} Hospital.".format(patient.patient_name, self.hospital_name)
            print "="*60
        return self


#create some hosiptals
dorthea_dix = Hospital("Dorthea Dix", 5)
tempken = Hospital("Tempken Mercy", 8)
#create some patients
patient1 = Patient("Shannon Benton", "fennel")
patient2 = Patient("Stephanie Tilley", "penicillin")
patient3 = Patient("Mike Freeman", "anesthetics")
patient4 = Patient("Nikki Dietzen", "aspirin, penicillin")
patient5 = Patient("Belinda Sturms", "nuts")
patient6 = Patient("Lisa Wilson", "shellfish")
patient7 = Patient("Beth Zirkle", None)
patient8 = Patient("Laura Voelker", "anesthetics")
patient9 = Patient("Nate Fowler", None)
patient10 = Patient("JoAnn Morgan", "bleach")
patient11 = Patient("Faith Chef", None)

#admit some patients to dorthea_dix hospital
dorthea_dix.admit(patient1).admit(patient2).admit(patient3).admit(patient4).admit(patient5).display() #should show reached capacity, no vacancies  CORRECT

#admit another patient to dorthea_dix
dorthea_dix.admit(patient6)  #should politely advise no room available  CORRECT

#admit some patients to tempken hospital
tempken.admit(patient7).admit(patient8).admit(patient9).admit(patient10).display() #should show availability  CORRECT

#discharge a patient from dorthea_dix
dorthea_dix.discharge(patient3).display() #should show availability now  CORRECT

#view patient info
patient3.display() #should show bed=none  CORRECT

#discharge a patient from tempken
tempken.discharge(patient6) #should advise patient not found in that hospital  CORRECT

# admit a patient to dorthea_dix
dorthea_dix.admit(patient11) #bed opened up (line98 so should allow)
patient11.display()  #should show patient at dorthea_dix hospital, bed #3
dorthea_dix.display() #should show full capacity