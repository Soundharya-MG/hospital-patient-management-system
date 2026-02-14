import json
import os

# ================== CONSTANTS ==================

FILE_NAME = "patients.json"

ADMIN_USERNAME = "administration"
ADMIN_PASSWORD = "123456"

PATIENT_NOT_FOUND = "Patient Not Found"
PATIENT_EXISTS = "Patient ID already exists"
INVALID_AGE = "Invalid Age Input"
NO_RECORDS = "No Patient Records Found"


# ================== CUSTOM EXCEPTIONS ==================

class PatientNotFoundException(Exception):
    pass


class DuplicatePatientException(Exception):
    pass


# ================== HOSPITAL MANAGER CLASS ==================

class HospitalManager:

    def __init__(self):
        self.filename = FILE_NAME
        self.patients = self.load_data()

    # ---------- Load Data ----------
    def load_data(self):
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    # ---------- Save Data ----------
    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.patients, file, indent=4)

    # ---------- Add Patient ----------
    def add_patient(self):
        patient_id = input("Enter Patient ID: ").strip()

        if any(p["id"] == patient_id for p in self.patients):
            raise DuplicatePatientException(PATIENT_EXISTS)

        name = input("Enter Patient Name: ").strip()

        try:
            age = int(input("Enter Age: "))
            if age <= 0:
                raise ValueError
        except ValueError:
            print(INVALID_AGE)
            return

        diagnosis = input("Enter Diagnosis: ").strip()
        treatment = input("Enter Treatment Plan: ").strip()

        patient = {
            "id": patient_id,
            "name": name,
            "age": age,
            "diagnosis": diagnosis,
            "treatment": treatment
        }

        self.patients.append(patient)
        self.save_data()

        print("Patient Added Successfully ✅\n")

    # ---------- View Patients ----------
    def view_patients(self):
        if not self.patients:
            print(NO_RECORDS, "\n")
            return

        print("\n----- Patient List -----")
        for p in self.patients:
            print(f"ID: {p['id']}")
            print(f"Name: {p['name']}")
            print(f"Age: {p['age']}")
            print(f"Diagnosis: {p['diagnosis']}")
            print(f"Treatment: {p['treatment']}")
            print("----------------------------")
        print()

    # ---------- Search Patient ----------
    def search_patient(self):
        patient_id = input("Enter Patient ID to search: ").strip()

        for p in self.patients:
            if p["id"] == patient_id:
                print("Patient Found ✅")
                print(p, "\n")
                return

        raise PatientNotFoundException(PATIENT_NOT_FOUND)

    # ---------- Update Patient ----------
    def update_patient(self):
        patient_id = input("Enter Patient ID to update: ").strip()

        for p in self.patients:
            if p["id"] == patient_id:
                p["name"] = input("Enter New Name: ").strip()

                try:
                    age = int(input("Enter New Age: "))
                    if age <= 0:
                        raise ValueError
                    p["age"] = age
                except ValueError:
                    print(INVALID_AGE)
                    return

                p["diagnosis"] = input("Enter New Diagnosis: ").strip()
                p["treatment"] = input("Enter New Treatment Plan: ").strip()

                self.save_data()
                print("Patient Updated Successfully ✅\n")
                return

        raise PatientNotFoundException(PATIENT_NOT_FOUND)

    # ---------- Delete Patient ----------
    def delete_patient(self):
        patient_id = input("Enter Patient ID to delete: ").strip()

        for p in self.patients:
            if p["id"] == patient_id:
                self.patients.remove(p)
                self.save_data()
                print("Patient Deleted Successfully ✅\n")
                return

        raise PatientNotFoundException(PATIENT_NOT_FOUND)

    # ---------- Generate Report ----------
    def generate_report(self):
        if not self.patients:
            print(NO_RECORDS, "\n")
            return

        total_patients = len(self.patients)
        avg_age = sum(p["age"] for p in self.patients) / total_patients

        print("\n----- Hospital Report -----")
        print("Total Patients:", total_patients)
        print("Average Age:", round(avg_age, 2))
        print("----------------------------\n")


# ================== LOGIN SYSTEM ==================

def login():
    print("====== Hospital Management Login ======")
    username = input("Username: ")
    password = input("Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login Successful ✅\n")
        return True
    else:
        print("Invalid Credentials ❌\n")
        return False


# ================== MAIN PROGRAM ==================

def main():
    if not login():
        return

    manager = HospitalManager()

    while True:
        print("====== MENU ======")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Generate Report")
        print("7. Exit")

        choice = input("Enter Choice: ")

        try:
            if choice == "1":
                manager.add_patient()
            elif choice == "2":
                manager.view_patients()
            elif choice == "3":
                manager.search_patient()
            elif choice == "4":
                manager.update_patient()
            elif choice == "5":
                manager.delete_patient()
            elif choice == "6":
                manager.generate_report()
            elif choice == "7":
                print("Exiting Program 👋")
                break
            else:
                print("Invalid Choice ❗\n")

        except PatientNotFoundException as e:
            print(e, "\n")
        except DuplicatePatientException as e:
            print(e, "\n")


if __name__ == "__main__":
    main()
