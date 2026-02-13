def repeat_stuff(stuff, num_repeats=10):
    return stuff*num_repeats
lyrics = "Your Boat " + repeat_stuff("Row", 3)
song = repeat_stuff("Row")
print(lyrics, song)

