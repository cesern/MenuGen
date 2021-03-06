from django.conf.urls import patterns, url

urlpatterns = patterns(
    'menus.views.views',

    url(r'^$', 'landing', name='landing'),
    url(r'^home$', 'home', name='home'),

    url(r'^menugendata$', 'statistics', name='statistics'),
    url(r'^account$', 'account', name='account'),
    url(r'^generation/cta$', 'call_to_action', name='call_to_action'),
)

"""
    Pre generation
"""
urlpatterns += patterns(
    'menus.views.generation.pre_generation_views',

    url(r'^generate$', 'generate', name='generate'),
    url(r'^generate/select_profile$', 'generate_select_profile', name='generate_select_profile'),
    url(r'^generate/placements_detail$', 'generate_placements_detail', name='generate_placements_detail'),

    url(r'^update_gen_criteria', 'update_gen_criteria', name='update_gen_criteria'),
)

"""
    Post generation
"""
urlpatterns += patterns(
    'menus.views.generation.post_generation_views',

    url(r'^generation$', 'generation', name='generation'),
    url(r'^generation/shopping_list$', 'generation_shopping_list', name='generation_shopping_list'),
    url(r'^generation/shopping_list_pdf$', 'shopping_list_pdf', name='shopping_list_pdf'),
    url(r'^generation/meal_details/(?P<starter_id>\d+)-(?P<main_course_id>\d+)-(?P<dessert_id>\d+)$',
        'generation_meal_details',
        name='generation_meal_details'),
    url(r'^generation/unlike_recipe/(?P<recipe_id>\d+)$', 'unlike_recipe_message', name='unlike_recipe_message'),
    url(r'^generation/unlike_ingredient/(?P<ingredient_id>\d+)$', 'unlike_ingredient_message', name='unlike_ingredient_message'),
    url(r'^pics/(?P<recipe_id>\d+)', 'recipe_pic', name='pics'),
)

"""
    Authentication
"""
urlpatterns += patterns(
    'menus.views.auth.auth_views',

    url(r'^sign-in$', 'sign_in', name='sign_in'),
    url(r'^sign-up$', 'sign_up', name='sign_up'),
    url(r'^sign-out$', 'sign_out', name='sign_out'),
)

"""
    Profiles
"""
urlpatterns += patterns(
    'menus.views.profiles.profiles_views',

    url(r'^profiles$', 'index', name='profiles'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)$', 'profile', name='profile'),

    url(r'^profiles/new', 'new', name='profile_new'),
    url(r'^profiles/(?P<profile_id>[0-9]+)/detail$', 'detail', name='profile_detail'),
    url(r'^profiles/(?P<profile_id>[0-9]+)/edit$', 'edit', name='profile_edit'),
    url(r'^profiles/(?P<profile_id>[0-9]+)/remove$', 'remove', name='profile_remove'),

    url(r'^update_physio$', 'update_profile', name='update_physio'),
    url(r'^update_profile$', 'update_profile', name='update_profile'),
    url(r'^physiology$', 'physiology', name='physiology'),
    url(r'^regimes$', 'regimes', name='regimes'),
    url(r'^tastes$', 'tastes', name='tastes'),
    url(r'^update_tastes', 'update_tastes', name='update_tastes'),
    url(r'^tastes/unlike_recipe/(?P<recipe_id>\d+)$', 'unlike_recipe', name='unlike_recipe'),
    url(r'^tastes/unlike_ingredient/(?P<ingredient_id>\d+)$', 'unlike_ingredient', name='unlike_ingredient'),
    url(r'^tastes/unlike_family/(?P<family_id>\d+)$', 'unlike_ingredient_family', name='unlike_ingredient_family'),
    url(r'^tastes/relike_recipe/(?P<recipe_id>\d+)$', 'relike_recipe', name='relike_recipe'),
    url(r'^tastes/relike_ingredient/(?P<ingredient_id>\d+)$', 'relike_ingredient', name='relike_ingredient'),
    url(r'^tastes/relike_family/(?P<family_id>\d+)$', 'relike_family', name='relike_family'),
)

"""
    Profiles
"""
urlpatterns += patterns(
    'menus.views.menus.menus_views',

    url(r'^menus$', 'menus', name='menus'),
    url(r'^menus/new', 'new', name='menu_new'),
)
