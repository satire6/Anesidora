from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DTutorialObjectBase:
    Sandwiches = Enum('Rye, Cheese, Ham, PeanutButter')
    Fruit = Enum('Apple, Pear, Strawberries, Cherries')
    Cake = Enum('Carrot, Chocolate, Pound, Bundt, Rum')

    Meals = {0: (Sandwiches.Rye, Fruit.Pear, Cake.Pound),
             1: (Sandwiches.Ham, Fruit.Apple, Cake.Rum),
             2: (Sandwiches.Cheese, Fruit.Pear, Cake.Carrot),
             3: (Sandwiches.Rye, Fruit.Cherries, Cake.Chocolate),
             }
