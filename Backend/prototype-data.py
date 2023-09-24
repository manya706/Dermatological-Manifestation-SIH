import csv
import random

# List of predictions
predictions = [
    'Acne, or Rosacea',
    'Actinic Keratosis, or other Malignant Lesions',
    'Alopecia, or other Hair Diseases',
    'Atopic Dermatitis',
    'Bacterial Infections',
    'Benign Tumors',
    'Bullous Disease',
    'Connective Tissue Diseases',
    'Eczema',
    'Exanthems, or Drug Eruptions',
    'Fungal Infections',
    'Healthy or Benign growth',
    'Herpes, HPV, other STDs',
    'Lyme Diseasem, Infestations and Bites',
    'Melanoma Skin Cancer Nevi and Moles',
    'Nail Fungus or other Nail Disease',
    'Poison Ivy or Contact Dermatitis',
    'Psoriasis, Lichen Planus or related diseases',
    'Systemic Disease',
    'Urticaria Hives',
    'Vascular Tumors',
    'Vasculitis Photos',
    'Warts, or other Viral Infections'
]

# List of Indian pin codes
pin_codes = ['110001', '400001', '560001', '600001', '700001', '800001', '110002', '400002', '560002', '600002']

# Generate 60 rows of fake data
rows = []
for _ in range(60):
    total_time = round(random.uniform(10, 500), 2)  # Random total time in milliseconds
    pincode = random.choice(pin_codes)  # Random Indian pin code
    prediction = random.choice(predictions)  # Random prediction from the list
    confidence = random.uniform(93.322, 100) # Random confidence values
    # Append to the rows
    rows.append([total_time, pincode, prediction, confidence])

# Write to CSV
with open('Backend\predictions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Total Time (ms)', 'Pincode', 'Prediction', 'Confidence'])
    writer.writerows(rows)
