# ссылки на рецепты горячих блюд
import time

import requests
# разбирает весь док хтмл и хмл на части
from bs4 import BeautifulSoup
from time import sleep
# from fake_useragent import UserAgent
# анализатор хтмл кода, который обработает его и передаст его в суп для нормальной читабельности
import lxml

headers = {'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'}
# видим ключ, вставляем значение в урл
def change_food():
    categories = {'горячие блюда': 'goryachie_bliuda', 'салаты':'salad',
                'закуски':'zakuski', 'выпечка':'vypechka', 'десерты':'dessert',
                'напитки':'napitki', 'соусы':'sousy', 'заготовки':'zagotovki'}
    while True:
        changed_category = input(
        f'Выберите, рецепты какой категории из списка вы хотели бы получить:\n\
{str(list(categories.keys())).strip("[]")}\n') 
        if changed_category.lower() in categories.keys():
            return categories[changed_category.lower()]
        else:
            print('Некорректный ввод категории. Попробуйте еще раз.')
            continue


def get_url():
    for count in range(1, 2):
        url = f'https://povar.ru/list/{change_food()}/{count}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')  # html.parser(можно вместо лхмл)
        data = soup.find_all('div', class_='recipe')
        for i in data:
            recipe_url = 'https://povar.ru' + i.find('div', class_='h3').find('a').get('href')
            # делаю запрос уже с ссылки полученной в дате на рецепт для полной инфы рецепта
            yield recipe_url

def array():
    for recipe_url in get_url():   
        response = requests.get(recipe_url, headers=headers)   
        # sleep(3)
        soup = BeautifulSoup(response.text, 'lxml')
        data_describe_recipe = soup.find('div', class_="cont_area hrecipe")
        dish_name = data_describe_recipe.find('a', class_='stepphotos').get('title')
        dish_cooking_time = data_describe_recipe.find('span', class_='duration').text
        #картинка блюда
        dish_img_url = data_describe_recipe.find('a', class_='stepphotos').get('href')
        # один ингредиент собираем
        ingredient_name = data_describe_recipe.find(
            'ul', class_='detailed_ingredients no_dots').find_all('span', class_='name') 
        mass_value = data_describe_recipe.find(
            'ul', class_='detailed_ingredients no_dots').find_all('span', class_='value')
        measure_of_value = data_describe_recipe.find(
            'ul', class_='detailed_ingredients no_dots').find_all('span', class_='u-unit-name')
        # все ингредиенты
        ingredients = ''
        # пришлось создать список строк склейки элементов после вычленения всех элементов в списке с тэгами
        for ing, val, meas in zip(ingredient_name, mass_value, measure_of_value):
            ingredients += ing.text.rstrip() + ': ' + val.text + ' ' + meas.text

        recipe_steps = data_describe_recipe.find_all('div', class_='detailed_step_description_big')
        recipe_steps2 = data_describe_recipe.find_all('span', class_='detailed_full')
        steps = [step.text for step in recipe_steps]  
        steps2 = [step.text for step in recipe_steps2]

        descr_recipe = ''
        if steps == []:
            for step in list(steps2):
                descr_recipe += step        
        elif steps != []:
            for step in list(steps):
                descr_recipe += step
           
        yield dish_name, dish_cooking_time, ingredients, descr_recipe, dish_img_url, recipe_url 
    
    



# if __name__ == '__main__':
    # # print(change_food())
    # print(array())
