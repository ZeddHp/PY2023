import pandas as pd

file_list = ['LV.txt', 'ENG.txt']
file_lv = file_list[0]
file_eng = file_list[1]

file_frequencies = {}

for file_name in file_list:
    with open(f'../Data/{file_name}', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        letter_frequency = {}

        for line in lines:
            line = line.lower()

            for char in line:
                if char.isalpha():
                    if char in letter_frequency:
                        letter_frequency[char] += 1
                    else:
                        letter_frequency[char] = 1

        file_frequencies[file_name] = letter_frequency

file_lv_frequency = file_frequencies[file_lv]
file_eng_frequency = file_frequencies[file_eng]

# Combine the frequencies of both files into one DataFrame
df = pd.DataFrame({'Latvian': file_lv_frequency,
                  'English': file_eng_frequency})
df = df.fillna(0)  # Replace NaN values with 0 for missing letters
df = df.astype(int)  # Convert frequencies to integers

# Calculate the total frequencies for each language
total_lv = df['Latvian'].sum()
total_eng = df['English'].sum()

# Calculate the percentages of frequencies for each language
df['Latvian (%)'] = df['Latvian'] / total_lv * 100
df['English (%)'] = df['English'] / total_eng * 100

# Format the percentages with desired precision
df['Latvian (%)'] = df['Latvian (%)'].map('{:.1f}%'.format)
df['English (%)'] = df['English (%)'].map('{:.1f}%'.format)

# Format the DataFrame with percentage values
df = df[['Latvian (%)', 'English (%)']]
df = df.sort_values(by='Latvian (%)', ascending=False)

# Display the frequencies in the desired format
print(df)
