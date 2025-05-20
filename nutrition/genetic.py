#Import numpy library
import pandas as pd
import numpy as np
import random
import copy

# константы генетического алгоритма

POPULATION_SIZE = 200   # количество индивидуумов в популяции
P_CROSSOVER = 0.8       # вероятность скрещивания
P_MUTATION = 0.1      # вероятность мутации индивидуума
MAX_GENERATIONS = 40

# константы задачи

#target_calories = 600  # Целевая калорийность на приём пищи
min_proteins = 20      # Минимум белков в граммах
min_fats = 15          # Минимум жиров в граммах
min_carbs = 50         # Минимум углеводов в граммах


#name, 
# price - цена за 100г, 
# gram_Prot - белки,  
# gram_Fat - жиры, 
# gram_Carb - угледводы, 
# minPortion - минимальная допустимая порция, 
# maxPortion - максимальная допустимая порция
# характеристики указаны за 100г
products_table = pd.DataFrame.from_records([

    ['Chicken breast', 145, 31, 3.6, 0, 100, 200],
    ['Cheddar cheese', 230, 25, 33, 1.3, 10, 30],
    ['Oatmeal', 39, 17, 7, 66, 50, 100],
    ['Apple', 42, 0.3, 0.2, 14, 100, 200],
    ['Almond', 200, 21, 49, 22, 10, 30],

    ['Banana', 15, 1.1, 0.3, 22, 50, 150],
    ['Ananas', 35, 0.5, 0.1, 13, 50, 70],
    ['Grapes', 35, 0.1, 0.5, 13, 50, 150],
    ['Pasta', 20, 5, 1.1, 25, 50, 90],
    ['Salmon', 208, 20, 13, 0, 100, 200],
    ['Carrot', 7, 0.9, 0.2, 10, 50, 75],
    ['Rice', 15, 2.4, 0.3, 28, 50, 130],
    ['Egg', 17, 13, 10, 1, 50, 100],
    ['Avocado', 46, 2, 15, 9, 30, 70],
    ['Potato', 6, 1.9, 0.1, 20, 50, 200],
    ['Spinach', 179, 2.9, 0.4, 3.6, 50, 80],
    ['Hoummous', 150, 7, 25, 11, 24, 55],
])

products_table.columns = ['name', 'price', 'gram_Prot', 'gram_Fat', 'gram_Carb', 'minPortion', 'maxPortion']

def generate_initial_population(size):
    population = []
    for _ in range(size):
        chromosome = []
        selected_products = random.sample(list(products_table.iterrows()), 5)
        for _, product in selected_products:
            portion = random.uniform(product['minPortion'], product['maxPortion'])
            chromosome.append({
                'name': product['name'],
                'price': product['price'],
                'proteins': product['gram_Prot'],
                'fats': product['gram_Fat'],
                'carbs': product['gram_Carb'],
                'portion': portion
            })
        population.append(chromosome)
        
    return population

def fitness_function(chromosome, target_calories):
    total_calories = 0
    total_proteins = 0
    total_fats = 0
    total_carbs = 0
    total_cost = 0
    
    #print(chromosome)

    for product in chromosome:  # Извлекаем продукт и генерируем порцию

        total_proteins += product['proteins'] * (product['portion'] / 100)
        total_fats += product['fats'] * (product['portion'] / 100)
        total_carbs += product['carbs'] * (product['portion'] / 100)
        total_calories += (total_proteins * 4) + (total_fats * 9) + (total_carbs * 4)
        total_cost += product['price'] * (product['portion'] / 100)  # цена за порцию
    
    # Оценка по калориям
    fitness = abs(target_calories - total_calories)
    
    # Штраф за недостаток белков, жиров, углеводов
    if total_proteins < min_proteins:
        fitness += (min_proteins - total_proteins) * 25
    if total_fats < min_fats:
        fitness += (min_fats - total_fats) * 5
    if total_carbs < min_carbs:
        fitness += (min_carbs - total_carbs) * 5

        # Учет разнообразия
    unique_products = set(product['name'] for product in chromosome)
    diversity_penalty = max(0, 3 - len(unique_products))  # Штраф за недостаток уникальности
    fitness += diversity_penalty * 95  # Умножаем штраф на 20, чтобы сделать его более заметным

    # Дополнительный бонус за присутствие мяса
    if any(product['name'] in ["Chicken breast", "Salmon"] for product in chromosome):
        fitness -= 250  # Уменьшаем фитнес за присутствие мяса

    # Включаем стоимость в расчет фитнеса (чем выше стоимость, тем хуже фитнес)
    fitness += total_cost * 0.35  # Умножаем стоимость на 7 для усиления влияния

    return fitness

def selection(population, fitnesses):
    # Простой вариант — турнирный отбор
    selected = []
    for _ in range(len(population)):
        idx1, idx2 = random.sample(range(len(population)), 2)
        if fitnesses[idx1] < fitnesses[idx2]: # поменять на <
            selected.append(population[idx1])
        else:
            selected.append(population[idx2])
    return selected

#двухточечный кроссовер
def two_point_crossover(parent1, parent2):
    if random.random() < P_CROSSOVER:
        point = random.randint(2, len(parent1) - 1)  # хотя бы один элемент должен оставаться в каждом родителе
        #print(point)
        # # Создаем детей путем комбинирования родителей
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    else:
        return parent1, parent2

def increase_decrease_mutation(chromosome):
    if random.random() < P_MUTATION:
        # Выбираем случайный индекс для изменения
        index = random.randint(0, len(chromosome) - 1)
        product = chromosome[index]
        
        # Случайное изменение значения
        mutation_factor = random.choice([-0.1, 0.1])  # Увеличиваем или уменьшаем на 10%
        for key in product:
            if key != 'name':  # Не меняем имя продукта
                product[key] += product[key] * mutation_factor
                
    return chromosome


def generate_meal_plan(health_profile, calorie_goal):

    population = generate_initial_population(POPULATION_SIZE)
    p1 = copy.deepcopy(population)


    import matplotlib.pyplot as plt

    # Переменные для хранения значений приспособленности
    maxFitnessValues = []
    meanFitnessValues = []
    sm = 0
    population = p1
    #print(p1)
    #population = generate_initial_population(POPULATION_SIZE)

    for generation in range(MAX_GENERATIONS):
        fitnesses = [fitness_function(chromosome, calorie_goal) for chromosome in population]

        # Сбор максимального и среднего значений фитнеса
        max_fitness = min(fitnesses)
        mean_fitness = sum(fitnesses) / len(population)  # Используем population для вычисления среднего

        maxFitnessValues.append(max_fitness)
        meanFitnessValues.append(mean_fitness)

        population = selection(population, fitnesses)

        ELITE_SIZE = 4  # сколько лучших сохранить

        # Отбираем лучших по фитнесу
        elite_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])[:ELITE_SIZE]
        elite_individuals = [copy.deepcopy(population[i]) for i in elite_indices]


        new_population = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1]
            child1, child2 = two_point_crossover(parent1, parent2)
            new_population.append(increase_decrease_mutation(child1))
            new_population.append(increase_decrease_mutation(child2))
            
        population = new_population[:-ELITE_SIZE] + elite_individuals
        
        # Финальная оценка
    fitnesses = [fitness_function(chromosome, calorie_goal) for chromosome in population]
    best_solution = population[fitnesses.index(min(fitnesses))]
    print(f"Поколение {generation}: Мин приспособ. = {max_fitness}, Средняя приспособ.= {mean_fitness}")

    for item in best_solution[:5]:
        formatted_item = {key: (f"{value:.4f}" if isinstance(value, float) else value) for key, value in item.items()}
        
        sm += float(f"{item['price']:.4f}")
        print(formatted_item)
    print(sm)
    

    #plt.plot(maxFitnessValues, color='red', label='Минимальная приспособленность')
    #plt.plot(meanFitnessValues, color='green', label='Средняя приспособленность')
    #plt.xlabel('Поколение')
    #plt.ylabel('Приспособленность')
    #plt.title('Зависимость максимальной и средней приспособленности от поколения')
    #plt.legend()
    #plt.show()
    return f"Вы выбрали '{health_profile}', цель: {calorie_goal} калорий."

    

generate_meal_plan("нет", 800)

