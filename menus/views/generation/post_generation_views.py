import datetime
import logging
import time
from functools import reduce

import numpy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import menugen.defaults as defaults
from menus.algorithms.dietetics import Calculator
from menus.algorithms.model.menu.menu_manager import MenuManager
from menus.algorithms.run import run_standard
from menus.algorithms.utils.config import Config
from menus.data.generator import generate_planning_from_list, generate_planning_from_matrix
from menus.models import Recipe, Profile, Ingredient

logger = logging.getLogger("menus")


def generation(request):
    """ Profile values are accessible from current session
        ex:
        WhateverAlgo(request.session['sex'], request.session['age'], request.session['height'], request.session['weight'])
        or
        WhateverAlgo2(request.session['budget'], request.session['difficulty'], request.session['nb_days'])
        """

    """ TODO:
    Here should be called the algorithm
    generating the structure containing the meals
    should be passed to the rendered view """

    nb_days = int(request.session.get('nb_days', 7))

    """ Default values """
    nb_dishes = 3
    nb_meals = 2

    if 'matrix' in request.session:
        matrix = request.session['matrix']
        nb_meals_menu = numpy.sum(matrix)
    else:
        nb_meals_menu = nb_meals * nb_days

    today = datetime.date.today()

    user_exercise = request.session.get('exercise', defaults.EXERCISE)
    user_age = int(request.session.get('age', defaults.AGE))
    user_weight = int(request.session.get('weight', defaults.WEIGHT))
    user_height = int(float(request.session.get('height', defaults.HEIGHT / 100)) * 100)
    user_sex = Calculator.SEX_F if request.session.get('sex') is 1 else Calculator.SEX_H
    user_birthday = datetime.date(year=today.year - user_age, month=today.month, day=today.day)
    if request is not None:
        account = request.user.account
        profile = account.profile
        profile_list = list(account.guests.all())
        profile_list.append(profile)
        logger.info('Crafted profile list from user profiles.')
    else:
        profile_list = [Profile(weight=user_weight, height=user_height, birthday=user_birthday, sex=user_sex,
                                activity=user_exercise)]
        logger.info('Crafted profile list from request data.')
    logger.info('Profiles at generation: %r.' % profile_list)
    needs_list = [Calculator.estimate_needs_profile(profile) for profile in profile_list]
    needs = reduce(lambda x, y: x + y, needs_list)
    logger.info("Final needs: %r" % needs)

    Config.parameters[Config.KEY_MAX_DISHES] = nb_meals_menu * nb_dishes
    logger.info("Max dishes set to %d." % Config.parameters[Config.KEY_MAX_DISHES])
    Config.update_needs(needs, nb_days)

    # Initialising MenuManager with appropriate meals for profile(s)
    MenuManager.new(profile_list)
    menu = run_standard(None, time.ctime())
    if len(menu.genes) < nb_meals_menu:
        pass  # FIXME: Remove after investigation

    if 'matrix' in request.session:
        matrix = request.session['matrix']
        planning = generate_planning_from_matrix(matrix, menu)
    else:
        planning = generate_planning_from_list(nb_days, nb_meals, menu)

    shopping_list = []
    for meal_time in planning:
        for meal in meal_time:
            if meal:
                print(meal)
                main_course = meal['main_course']
                for i in main_course.ingredients.all():
                    shopping_list.append(i.name)

    return render(request, 'menus/generation/generation.html', {
        'planning': planning,
        'days_range': range(0, nb_days),
        'shopping_list': shopping_list
    })


def replace_if_none(var, default):
    if var is None:
        var = default
    return var


def generation_meal_details(request, starter_id, main_course_id, dessert_id):
    """ Here should be loaded a meal from db according to the given ids
    A meal is composed of a starter, a main course and a dessert """

    starter = Recipe.objects.get(pk=starter_id)
    main = Recipe.objects.get(pk=main_course_id)
    dessert = Recipe.objects.get(pk=dessert_id)

    meal = {'starter': starter, 'main_course': main, 'dessert': dessert}
    return render(request, 'menus/generation/meal_details.html', {'meal': meal})


@login_required
def unlike_recipe_message(request, recipe_id):
    """ Message after unliking a recipe """
    recipe = Recipe.objects.get(id=recipe_id)
    profile = request.user.account.profile;
    profile.unlikes_recipe.add(recipe);
    return render(request, 'menus/generation/unlike_recipe_popup.html', {
        'recipe_name': recipe.name
    })


@login_required
def unlike_ingredient_message(request, ingredient_id):
    """ Message after unliking an ingredient """
    ingredient = Ingredient.objects.get(id=ingredient_id)
    profile = request.user.account.profile;
    profile.unlikes_ingredient.add(ingredient)
    return render(request, 'menus/generation/unlike_ingredient_popup.html', {
        'ingredient_name': ingredient.name
    })
