import matplotlib.pyplot as plt
import random
number_a = list(range(1,13))
number_b = random.sample(range(1000), 12)
plt.plot(number_a,number_b)
plt.show()