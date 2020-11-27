#Choices for charfields in profile app.

GENDER_CHOICES=(
    ('Male','Male'),
    ('Female','Female'),
    ('Non-Binary',"Non Binary"),
    ('N/A', 'Prefer not to say',)
)

T_SHIRT_SIZE_CHOICES=(
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL')
)

FIELD_OF_STUDY_CHOICES=(
    ('School Student', 'School Student'),
    ('Bachelor of Science', 'Bachelor of Science'),
    ('Bachelor of Arts', 'Bachelor of Arts'),
    ('Bachelor of Technology', 'Bachelor of Technology'),
    ('Bachelor of Commerce', 'Bachelor of Commerce'),
    ('Master of Science', 'Master of Science'),
    ('Master of Arts', 'Master of Arts'),
    ('Master of Technology', 'Master of Technology'),
    ('Master of Commerce', 'Master of Commerce'),
    ('Other', 'Other'),
)

CLASS_CHOICES=(
    (' ',' '),
    ('S1R','S1R'),('S3R','S3R'),('S5R','S5R'),('S7R','S7R'),
    ('S1LA','S1LA'),('S1LB','S1LB'),('S3LA','S3LA'),('S3LB','S3LB'),('S5LA','S5LA'),('S5LB','S5LB'),('S7LA','S7LA'),('S7LB','S7LB'),
    ('S1EA','S1EA'),('S1EB','S1EB'),('S3EA','S3EA'),('S3EB','S3EB'),('S5EA','S5EA'),('S5EB','S5EB'),('S7EA','S7EA'),('S7EB','S7EB'),
    ('S1CA','S1CA'),('S1CB','S1CB'),('S3CA','S3CA'),('S3CB','S3CB'),('S5CA','S5CA'),('S5CB','S5CB'),('S7CA','S7CA'),('S7CB','S7CB'),
    ('S1MA','S1MA'),('S1MB','S1MB'),('S3MA','S3MA'),('S3MB','S3MB'),('S5MA','S5MA'),('S5MB','S5MB'),('S7MA','S7MA'),('S7MB','S7MB'),   
)

STATE_OF_RESIDENCE_CHOICES = (
    ('Outside India', 'Outside India'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Andaman And Nicobar Islands', 'Andaman And Nicobar Islands'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra And Nagar Haveli And Daman And Diu', 'Dadra And Nagar Haveli And Daman And Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu And Kashmir', 'Jammu And Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)

EDUCATIONAL_STATUS_CHOICES = (
    ('High School', 'High School'),
    ('Bachelors', 'Bachelors'),
    ('Masters', 'Masters'),
    ('PhD', 'PhD'),
)

YEAR_OF_GRADUATION_CHOICES = (
    (2018, 2018),
    (2019, 2019),
    (2020, 2020),
    (2021, 2021),
    (2022, 2022),
    (2023, 2023),
    (2024, 2024),
    (2025, 2025),
)

TEAM_STATUS_CHOICES = (
    ('No Team', 'I want to participate alone'),
    ('Need Team', 'I would like to participate as a team, but I haven\'t found a team yet'),
    ('Has Team', 'I would like to participate as a team and I already have a team.'),
)

BOOLEAN_CHOICES = (
    (0,'No'),
    (1,'Yes'),
)

AVATAR_CHOICES = (
    ('antman', 'Ant-Man'),
    ('arrow', 'Arrow'),
    ('batman', 'Batman'),
    ('blackpanther', 'Black Panther'),
    ('blackwidow', 'Black Widow'),
    ('cap', 'Captain America'),
    ('cyclops', 'Cyclops'),
    ('daredevil', 'Daredevil'),
    ('deadpool', 'Deadpool'),
    ('deathstroke', 'Deathstroke'),
    ('drstrange', 'Dr. Strange'),
    ('falcon', 'The Falcon'),
    ('flash', 'The Flash'),
    ('gamora', 'Gamora'),
    ('gwenstacy', 'Gwen Stacey'),
    ('hawkeye', 'Hawk Eye'),
    ('hulk', 'The Hulk'),
    ('ironman', 'Iron Man'),
    ('loki', 'Loki'),
    ('nightwing', 'Nightwing'),
    ('robin', 'Robin'),
    ('spiderman', 'Spider Man'),
    ('starlord', 'Starlord'),
    ('superman', 'Superman'),
    ('thor', 'Thor'),
    ('venom', 'Venom'),
    ('vision', 'Vision'),
    ('warmachine', 'War Machine'),
    ('wintersoldier', 'The Winter Soldier'),
    ('wolverine', 'Wolverine'),
    ('wonderwoman', 'Wonder Woman'),
    ('zoom', 'Zoom'),
    ('nota', 'None of the Above'),
)