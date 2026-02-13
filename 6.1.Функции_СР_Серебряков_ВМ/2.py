def get_force(m, a):
    return m*a
train_mass, train_accelerator, train_distance = map(int, input().split())
print("Поезд GE поставляет "+str(get_force(train_mass, train_accelerator))+" ньютонов силы")
def get_energy(m):
    c = 3*10**8
    return  m*(c**2)
bomb_energy = get_energy(1)
print(f"1 кг бомбы составляет {bomb_energy} Джоулей")

def get_work(m,a,s):
    return get_force(m, a) * s
train_work = get_work(train_mass, train_accelerator, train_distance)
print(f"Поезд выполняет {train_work} Джоулей за {train_distance} метров.")
