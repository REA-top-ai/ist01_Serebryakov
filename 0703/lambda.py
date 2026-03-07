contains_a = lambda my_input: "a" in my_input
print(contains_a("hello"))  
print(contains_a("banana"))
long_string = lambda my_input: len(my_input) > 12
print(long_string("short string"))
print(long_string("this is a veryyyyy looooong string"))
end_in_a = lambda my_input: my_input[-1] == "a"
print(end_in_a("apple"))
print(end_in_a("banana"))


even_or_odd = lambda num: "чётное" if num % 2 == 0 else "нечётное"
print(even_or_odd(4))
print(even_or_odd(7))
multiple_of_three = lambda num: "кратное трем" if num % 3 == 0 else "не кратное"
print(multiple_of_three(9))
print(multiple_of_three(10))
rate_movie = lambda raiting: "Мне понравился этот фильм" if raiting > 8.5 else "Этот фильм был не очень хорошим"
print(rate_movie(9.0))
print(rate_movie(7.5))