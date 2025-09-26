from datetime import date
import random


# Global set to store generated numbers
generated_numbers = set()

def generate_unique_number():
    if len(generated_numbers) >= 100:
        return "All numbers between 1 and 100 have been generated."
    
    while True:
        num = random.randint(100, 600)
        if num not in generated_numbers:
            generated_numbers.add(num)
            return num
            
            
def generate_partone():
    tday = date.today()
    vid = "VM"
    one =vid+str(tday.day)+str(tday.month)+str(tday.year)[2:]+"/"
    return one
    
def visitoridgen():
    part2 = str(generate_unique_number())
    part1 = generate_partone()
    return part1+part2
