import os
import glob
from tika import parser
import csv

# path = '/home/hamza/Desktop/sease/resume'
# cvpath = os.chdir('/home/hamza/Desktop/sease/resume')
# file = glob.glob('*.*')
# output_file = '/home/hamza/Desktop/sease/example_input/documents_10k.tsv'
# with open(output_file, 'w', newline='', encoding='utf-8') as tsv_file:
#     writer = csv.writer(tsv_file, delimiter='\t')
#     # writer.writerow(['Filename', 'Content'])
#
#     for cv in file:
#         parsed = parser.from_file(cv)
#         content = parsed["content"].strip().replace('\n', '')
#         writer.writerow([content])
#
#
# print(f"Data saved to {output_file}")
# experiment result
cvpath = os.chdir('/home/spyresync/Desktop/project/resume')
file = glob.glob('*.*')
output_file = '/home/spyresync/Desktop/project/example_input/documents_10k.tsv'

with open(output_file, 'w', newline='', encoding='utf-8') as tsv_file:
    writer = csv.writer(tsv_file, delimiter='\t')

    for cv in file:
        parsed = parser.from_file(cv)

        if parsed is not None and 'content' in parsed and parsed['content'] is not None:
            content = parsed['content'].strip().replace('\n', '')
            writer.writerow([content])
        else:
            print(f"Failed to parse {cv}")

print(f"Data saved to {output_file}")
