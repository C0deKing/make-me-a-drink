import requests
from bs4 import BeautifulSoup as soup
import spacy
import json
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import Span
nlp = spacy.load('en_core_web_sm')
from string import punctuation
import numbers
import sys, os

# path = './'
# dirs = os.listdir( path )

# # This would print all the files and directories
# for file in dirs:
#    print(file)

listofdrinks = [
"https://www.allrecipes.com/recipe/85326/white-russian/",
"https://www.allrecipes.com/recipe/283225/mezcal-paloma/",
"https://www.allrecipes.com/recipe/214634/sicilian-sunset/",
"https://www.allrecipes.com/recipe/160773/the-champagne-cocktail/",
"https://www.allrecipes.com/recipe/145917/annex-theater-champagne-cocktail/",
"https://www.allrecipes.com/recipe/88774/wallaby-darned/",
"https://www.allrecipes.com/recipe/183285/holiday-mimosa/",
"https://www.allrecipes.com/recipe/25845/cosmopolitan/",
"https://www.allrecipes.com/recipe/110218/peach-cosmo/",
"https://www.allrecipes.com/recipe/216450/captains-mojito/",
"https://www.allrecipes.com/recipe/220567/sugar-free-mojito-punch/",
"https://www.allrecipes.com/recipe/229643/mojito-perfecto/",
"https://www.allrecipes.com/recipe/168102/mint-cucumber-mojitos/",
"https://www.allrecipes.com/recipe/20103/shaggys-manhattan/",
"https://www.allrecipes.com/recipe/158307/whiskey-sours/",
"https://www.allrecipes.com/recipe/162397/classic-old-fashioned/",
"https://www.allrecipes.com/recipe/160596/rob-roy/"
]

def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    page = soup(req.text, parser)
    return json.loads("".join(page.find("script", {"type":"application/ld+json"}).contents))

def get_name(jsonld):
    try:
        name = jsonld['name']
    except:
        name = jsonld[1]['name']
    
    lst = []
    for i, each in enumerate(name.lower().split()):
        lst.append(each.capitalize())
    name = ''.join(lst)
    
    return name

def get_ingredients_allrecipes_hardcode(jsonld):
    try:
        ingredients = jsonld['recipeIngredient']
    except:
        ingredients = jsonld[1]["recipeIngredient"]
        
    core = []
    garnish = []
    measurement = ['ounce', 'ounces', 'cup', 'cups', 'tablespoon', 'tablespoons', 'fluid', 'dash', 'sprig', 'teaspoon', 'teaspoons', 'jigger', 'jiggers']
    descriptors = ['fresh ', 'flavored ']
    liquors = ['whiskey', 'gin', 'vodka', 'tequila', 'rum', 'bourbon', 'brandy']
    
    for i, ingredient in enumerate(ingredients):
        
        main = None
        if ',' in ingredient:
            ing = ingredient.split(',')
            for each in ing:
                if each[0].isnumeric():
                    main = each
            ingredient = main
            
        ingredient = ingredient.encode("ascii", errors="ignore").decode()
        
        paren = ingredient[ingredient.find('('):ingredient.find(')')+1]
        ingredient = ingredient.replace(paren, '')
        
        # Replacing quantifiers from the front of the sentence
        lst = [ing.replace('-',' ') for ing in ingredient.split()]
        while lst[0].isnumeric() or any([x == lst[0] for x in measurement]):
            lst.pop(0)
        word = ' '.join(lst)
        
        # Replacing descriptors from sentence
        for d in descriptors:
            word = word.replace(d, '')
            
        if 'syrup' in word:
            wrdlst = word.split()
            i = wrdlst.index('syrup')
            try:
                wrd = wrdlst[i-1].capitalize()
                core.append('(SyrupOfFn %s)' % wrd)

            except:
                core.append("Syrup")
            continue
        
        # Getting juice
        if 'juice' in word:
            # Two ways to do this, one with juice, the other without
            nojuice = word.replace('juice', '')
            
            nojuicelst = []
            for token in nlp(nojuice).noun_chunks:
                nojuicelst.append(token.text)
            nojuicelst = [x.capitalize() for x in nojuicelst]
            
            fruit = ' '.join(nojuicelst)
            
            core.append('(JuiceOfFn %s)' % fruit)
            continue
        
        # Getting just ice
        if 'ice' in word or 'ice cube' in word:
            core.append('Ice')
            continue
            
        # Getting garnish
        if 'garnish' in word:
            word = word.replace('garnish','').replace('for', '')
            lst = [x.capitalize() for x in word.split()]
            core.append(''.join(lst))
            garnish.append(''.join(lst))
            continue
        
        if 'bitter' in word:
            wrdlst = word.split()
            try:
                i = wrdlst.index('bitter')
            except:
                i = wrdlst.index('bitters')
                
            try:
                wrd = wrdlst[i-1].capitalize()
                core.append('(BittersOfFn %s)' % wrd)
            except:
                core.append("Bitters")
            continue
        
        # Getting liqueurs
        if 'liqueur' in word:
            liq = word.replace('liqueur','')
            liq = [x.capitalize() for x in liq.split()]
            l = ' '.join(liq)
            
            core.append('(LiqueurOfFn %s)' % l)
            continue
            
        # Getting distilled spirits
        hasspirits = False
        for l in liquors:
            if l in word:
                liq = [x.capitalize() for x in word.split()]
                full = ''.join(liq)
                core.append(full)
                hasspirits = True
                break
        if hasspirits == True:
            continue
        
        ok = [x.capitalize() for x in word.split()]
        ok = ''.join(ok)
        core.append(ok)

    res = [] 
    [res.append(x) for x in core if x not in res] 
            
    return res, garnish

def into_krf(jsonld):
    ingredients, garnish = get_ingredients_allrecipes_hardcode(jsonld)
    name = get_name(jsonld)
    
    query = []
    for i in ingredients:
        query.append("(ingredientOf %s %s)" % (i, name))
    for g in garnish:
        query.append("(isGarnish %s)" % g)
        
    return query

def make_krf(listofdrinks):

    with open("../knowledge_base/cocktails2.krf", mode='w') as file:
        file.write("(in-microtheory IngredientsMt)\n")
        file.write("(genlMt MakeMeADrinkMt IngredientsMt)\n")
        
        for i, url in enumerate(listofdrinks):
            jsonld = get_ld_json(url)
            n = get_name(jsonld)
            name = "(isa %s CocktailDrink)" % n
            u = "(url %s %s )" % (n, url)
            q = into_krf(jsonld)

            cast = []
            cast.append(name)
            cast.append(u)
            print(cast)
            for item in q:
                cast.append(item)

            for line in cast:
                file.write(line + '\n') 

make_krf(listofdrinks)


# if __name__ == "__main__":
#     url = sys.argv[1]
#     try:
#         mode = sys.argv[2]
#     except:
#         mode = 'w'
