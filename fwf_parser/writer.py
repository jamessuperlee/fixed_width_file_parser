import csv

def write_csv(rows, output_file, encoding):

    with open(output_file, 'w', newline='', encoding=encoding) as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
