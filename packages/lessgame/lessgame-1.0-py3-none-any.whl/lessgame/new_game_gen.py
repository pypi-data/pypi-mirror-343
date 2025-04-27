import random

def binary_by_12(dec):
    b = bin(dec)
    b = str(b)[2::]
    added_0 = (12 - len(b)) * "0"
    b = added_0 + b
    return b

def turn_by_90_deg(num):

    binary = binary_by_12(num)
    bin_arry = list(binary)

    # 000000000001
    # 000010000000
    #  +-+-+
    #  | | |
    #  +-+-+
    #  | | |
    #  +-+-+
    ##
    #  +0+1+
    #  2 3 4
    #  +5+6+
    #  7 8 9
    #  +10+11+

    new_arry = ["0"] * 12

    # left outside
    new_arry[0], new_arry[4], new_arry[11], new_arry[7] = (
        bin_arry[7],
        bin_arry[0],
        bin_arry[4],
        bin_arry[11],
    )
    # right outside
    new_arry[1], new_arry[9], new_arry[10], new_arry[2] = (
        bin_arry[2],
        bin_arry[1],
        bin_arry[9],
        bin_arry[10],
    )
    # inside
    new_arry[3], new_arry[6], new_arry[8], new_arry[5] = (
        bin_arry[5],
        bin_arry[3],
        bin_arry[6],
        bin_arry[8],
    )

    new_n = "".join(new_arry)

    new_n = "0b" + new_n
    new_n = int(new_n, 2)

    return new_n


NUMBERS = [
    "000000000001", # short under
    "000000000011", # long under
    "000001001000", # L right down 
    "000001001000", # L right down
    "000000001001", # L right middle
    "000000001001", # L right middle
    "000000001001", # L right middle
    "000000001010", # L left middle
    "000000001010", # L left middle
    "000000001011", # short T 
    "000100100100", # snake 
    "000100100100", # snake
    
]

GOOD_NUMBERS = []

for num in NUMBERS:
    nnum = f"0b{num}"
    nnum = int(nnum,2)
    GOOD_NUMBERS.append(nnum)


def game_numbers():
    chossen = []
    temp_list = GOOD_NUMBERS[:] 
    for _  in range(9):
        random_ele = random.choice(temp_list)
        temp_list.remove(random_ele)
        chossen.append(random_ele) 
        
    for i in range(len(chossen)):
        r = random.randint(0, 3)
        for _ in range(r):
            chossen[i] = turn_by_90_deg(chossen[i])
    
    return chossen 