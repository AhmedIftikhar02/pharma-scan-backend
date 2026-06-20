# Cell 7: Write pharma_scan/data/drug_lexicon.py

lines = [
    "# In-memory drug lexicon: generic + common brand names\n",
    "\n",
    "DRUG_LEXICON = [\n",
    "    # Analgesics / Antipyretics\n",
    "    'Panadol', 'Paracetamol', 'Brufen', 'Ibuprofen', 'Aspirin', 'Disprin',\n",
    "    'Diclofenac', 'Voltaren', 'Ponstan', 'Mefenamic Acid', 'Tramadol',\n",
    "    # Antibiotics\n",
    "    'Amoxicillin', 'Augmentin', 'Azithromycin', 'Zithromax', 'Ciprofloxacin',\n",
    "    'Cipro', 'Metronidazole', 'Flagyl', 'Clarithromycin', 'Doxycycline',\n",
    "    'Cephalexin', 'Cefixime', 'Ceftriaxone', 'Ampicillin', 'Cloxacillin',\n",
    "    'Erythromycin', 'Trimethoprim', 'Levofloxacin', 'Moxifloxacin',\n",
    "    # Antacids / GI\n",
    "    'Omeprazole', 'Losec', 'Pantoprazole', 'Nexium', 'Esomeprazole',\n",
    "    'Ranitidine', 'Domperidone', 'Motilium', 'Metoclopramide', 'Flagyl',\n",
    "    'Buscopan', 'Hyoscine', 'Lactulose', 'Dulcolax', 'Bisacodyl',\n",
    "    # Antidiabetics\n",
    "    'Metformin', 'Glucophage', 'Glibenclamide', 'Glimepiride', 'Sitagliptin',\n",
    "    'Januvia', 'Insulin', 'Jardiance', 'Empagliflozin',\n",
    "    # Cardiovascular\n",
    "    'Amlodipine', 'Norvasc', 'Atenolol', 'Lisinopril', 'Losartan',\n",
    "    'Cozaar', 'Ramipril', 'Valsartan', 'Hydrochlorothiazide', 'Furosemide',\n",
    "    'Lasix', 'Spironolactone', 'Digoxin', 'Warfarin', 'Clopidogrel', 'Plavix',\n",
    "    'Atorvastatin', 'Lipitor', 'Rosuvastatin', 'Simvastatin',\n",
    "    # Respiratory\n",
    "    'Salbutamol', 'Ventolin', 'Budesonide', 'Pulmicort', 'Montelukast',\n",
    "    'Singulair', 'Cetirizine', 'Zyrtec', 'Loratadine', 'Chlorpheniramine',\n",
    "    'Prednisolone', 'Dexamethasone', 'Hydrocortisone',\n",
    "    # Vitamins / Supplements\n",
    "    'Vitamin C', 'Vitamin D', 'Vitamin B12', 'Folic Acid', 'Zinc',\n",
    "    'Calcium', 'Iron', 'Ferrous Sulphate', 'Multivitamin',\n",
    "    # CNS\n",
    "    'Diazepam', 'Valium', 'Alprazolam', 'Xanax', 'Sertraline', 'Zoloft',\n",
    "    'Fluoxetine', 'Prozac', 'Amitriptyline', 'Haloperidol', 'Risperidone',\n",
    "    # Antifungals / Antivirals\n",
    "    'Fluconazole', 'Diflucan', 'Clotrimazole', 'Acyclovir', 'Zovirax',\n",
    "]\n",
]

with open("pharma_scan/data/drug_lexicon.py", "w") as f:
    f.writelines(lines)

print("✅ drug_lexicon.py written.")