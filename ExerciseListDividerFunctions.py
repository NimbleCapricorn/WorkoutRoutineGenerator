# ExerciseList Divider Functions
def sliding_window(array, k):
    """give back k size subarrays of array using a sliding window"""
    for i in range(len(array)-k+1):
        yield array[i:i+k]
def divide_chunks(l, n):
    """Yield successive n-sized chunks from l.""" 
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]
