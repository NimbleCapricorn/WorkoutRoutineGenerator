#native xlsx writing:
#The output file below is a simple text representation of the generated workout program           
with open('Output.txt', 'w') as output_file:
    output_file.write(str(WeeklyTable))
    
WorkBook=Workbook('Output.xlsx')
for week in WeeksOfProgram:
    worksheet = WorkBook.add_worksheet(f"Week{week.ID}")
    for index, day in enumerate(Days):
        worksheet.merge_range(1, (6*index+1), 1, (6*index+6), Days[index])
    worksheet.add_table(1,2, (5*len(Days)),(windowsize+3), {'header_row':False})
    for index, day in enumerate(Days):
        worksheet.write_row((index*5+1), 3, ["Exercise", "Sets", "Reps", "PercentageOfOneRepMax","INOL"])
    for index, day in enumerate(week.ProgramDays):
        for exercise in day.ExerciseList:
            worksheet.write_row((3+index), 1, exercise)