celebs = ("Taylor Swift", "Lionel Messi", "The Weeknd", "Keanu Reeves", "Angelina Jolie")
ages = (36, 38, 36, 61, 50)

celebs_list = []
ages_list = []

#for celeb in celebs:
    #celebs_list.append(celeb)
i = 0
while i < len(celebs):
    celebs_list.append(celebs[i])
    ages_list.append(ages[i])
    i += 1

ages_lists = [age for age in ages]

celebs_dict = {"celebrities": celebs_list, "ages": ages_lists}

print(celebs_dict)

