# make-me-a-drink

The semantic web provides a vast amount of data that is distributed across the internet; included in that data is recipes, geographic data, cultural data, and much more. By combining the semantic web with classical knowledge, representation, and reasoning techniques one can make practical use of the power of the semantic web to provide rich experiences. Our KB system “Make Me a Drink” is designed to leverage the semantic web to inform cocktail enthusiasts on what cocktails they can make with the ingredients they have on hand. Furthermore we aim to be able to help cocktail enthusiasts decide on which ingredients they should purchase next.


# Getting Started

We provide all of the .krf files needed to load the project into companions. The suggested order of loading project files is as follows

- ontology.krf
- facts.krf
- cocktails.krf
- ingredients.krf

## Generating your own KRF files
Our project comes with a python script you can run to generate new KRF files based on recipes found on the internet. Follow the below instructions to invoke the script

1. Clone the github into a folder of your choice, then navigate to the directory ~/make-me-a-drink/ingestion.
2. Copy the url of your desired cocktail. The url must be from allrecipes.com.
3. Install dependencies `pip3 install -r requirements.txt`
4. Install Spacy Module `python3 -m spacy download en_core_web_sm`
5. Run
```
> python ingredients.py "your url here"
```
to add your drink to the cocktails.krf file that has all the drinks.

6. If you don't enter any url, the program will ask you if you want to rewrite the existing cocktails.krf file. This might be useful in the case where you screw up something in the file and would like to start over with a blank slate. If this is the intended purpose, enter 'y' when prompted; otherwise, enter 'n'.

## Evaluating the knowledge Base
In order to evaluate the knowledge stored in the knowledge base, you can run the following queries in companions

### To Find Makable Cocktails
```
(makeableCocktail ?cocktail ?ingredients)
```

### To Find possible drinks you can make (using the rules of cocktail making combined with stored cocktail recipes and substutitions)
```
(makeMeADrink ?instructions)
```

### To Find missing ingredients for cocktails you can not make
```
(ingredientsToBuyNext ?ingredients ?cocktail)
```