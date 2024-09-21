# Hospitals Management System (HMS) 🚑

## Overview

The Hospitals Management System (HMS) is a comprehensive solution developed on the Odoo framework to streamline and manage hospital operations efficiently. This module manages patients, doctors, and departments, integrating with Odoo's CRM for seamless customer relationship management. The project features advanced controls for users and managers, ensuring secure and intuitive access to hospital data.

## Features

### 1. Patient Management
- **Core Information**: 
  - First Name
  - Last Name
  - Birth Date
  - Address
  - Blood Type
  - Medical History (HTML)
  - CR Ratio
  - PCR Status
- **Image Upload**: Attach patient images.
- **Automatic Age Calculation**: Based on the patient's birth date.
- **Status Logs**: Tracks patient status (Undetermined, Good, Fair, Serious) with real-time logging of changes.
- **Conditional Field Management**:
  - PCR automatically checked if age < 30 with a warning message.
  - CR Ratio mandatory if PCR is checked.
  - Medical history hidden if age < 50.

### 2. Department & Doctors Management
- **Departments**:
  - Fields: Name, Capacity, Is Opened.
  - Patients linked to departments.
  - Prevent patients from being assigned to closed departments.
  - Department capacity dynamically shown on patient view.
  
- **Doctors**:
  - Fields: First Name, Last Name, Image.
  - Many-to-Many relationship with patients.
  - Doctors field is readonly until a department is selected for the patient.

### 3. Odoo CRM Integration
- Patients linked with Odoo's CRM customers via the `related_patient_id` field.
- **Unique Email Validation**: Prevent linking CRM customers and patients with the same email.
- Restricts the deletion of CRM customers who are linked to a patient.
- Enforces Tax ID requirement for CRM customers.

### 4. User Groups and Access Control
- **User**:
  - Create, Read, Update only their patients' records.
  - Read-only access to departments and doctors.
  - Cannot view doctors' menu or doctor fields in the patient form.
  
- **Manager**:
  - Full Create, Read, Update, Delete access for all patients, departments, and doctors.
  - Full visibility of all fields and menus.
