# make-me-a-drink

The semantic web provides a vast amount of data that is distributed across the internet; included in that data is recipes, geographic data, cultural data, and much more. By combining the semantic web with classical knowledge, representation, and reasoning techniques one can make practical use of the power of the semantic web to provide rich experiences. Our KB system “Make Me a Drink” is designed to leverage the semantic web to inform cocktail enthusiasts on what cocktails they can make with the ingredients they have on hand. Furthermore we aim to be able to help cocktail enthusiasts decide on which ingredients they should purchase next.


# Getting Started

We provide all of the .krf files needed to load the project into companions. The suggested order of loading project files is as follows

- ontology.krf
- facts.krf
- cocktails.krf
- ingredients.krf

In order to evaluate the knowledge stored in the knowledge base, you can run the following queries in companions

### To Find Makable Cocktails
```
(makeableCocktail ?cocktail ?ingredients)
```

### To Find possible drinks you can make (using the rules of cocktail making combined with stored cocktail recipes and substutitions)
```
(makeMeADrink ?instructions)
```

