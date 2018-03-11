from product import Product
from store import Store


#create a store
store1 = Store("Shannon's Shoemania", "Shannon Steen", "4325 S. Front St, Wilmington NC")

#create some products
shoes1 = Product(89.99, 'Janissah Wedge Sandals', '9 oz', 'Nine West', color='Taupe')
shoes2 = Product(89.00, 'Emmala', '7 oz', 'Nine West', color='Orange Multi')
shoes3 = Product(59.99, 'Longitano Sandals', '9 oz', 'Nine West', color='Black Silver')
shoes4 = Product(210.00, 'Hallden', '9 oz', 'Ted Baker', color='Palace Gardens')
shoes5 = Product(169.59, 'Rashi', '8 oz', 'Imagine Vince Camuto', color='Soft Gold')
shoes6 = Product(39.99, 'Rainaa', '9 oz', 'Bandolino', color='Gold Glamour')
shoes7 = Product(47.99, 'Rainaa', '9 oz', 'Bandolino', color='Gunmetal Glamour')
shoes8 = Product(84.95, 'Faelyn', '8 oz', 'Anne Klein', color='Tropical Black Multi')
shoes9 = Product(328.00, 'Licorice Too', '7 oz', 'Kate Spade', color='Multi Glitter')
shoes10 = Product(109.00, 'Ginette', '9 oz', 'Calvin Klein', color='Sandstorm')
shoes11 = Product(777.00, 'Sequined Pumps', '10 oz', 'Dolce & Gabbana', color='Black')
purse1 = Product(228.00, 'Kingston Drive Blossom Alessa', '13 oz', 'Kate Spade', color='Cream multi')
purse2 = Product(98.00, 'Blake Street Ditsy Blossom Mikey', '3 oz', 'Kate Spade', color='Black')
purse3 = Product(98.00, 'Blake Street Ditsy Blossom Mikey', '3 oz', 'Kate Spade', color='Watermelon')
purse4 = Product(117.99, 'Novelty East/West Boxed', '1 lb 10.8 oz', 'Calvin Klein', color='Cashew')
purse5 = Product(54.99, 'Card Holder', '2.6 oz', 'Michael Kors', color='Light Pewter')
purse6 = Product(54.99, 'Card Holder', '2.6 oz', 'Michael Kors', color='Soft Pink')

#add some products to store
store1.add_product(shoes1).add_product(shoes2).add_product(shoes3).add_product(shoes4).add_product(shoes5)
store1.add_product(shoes6).add_product(shoes7).add_product(shoes8).add_product(shoes9).add_product(shoes10)
store1.add_product(shoes11).add_product(purse1).add_product(purse2).add_product(purse3).add_product(purse4)
store1.add_product(purse5).add_product(purse6)

#apply a storewide brand sale
store1.brand_sale('Kate Spade', 20)
store1.brand_sale('Nine West', .30)

#check the inventory (should see sale price for Kate Spade AND Nine West brands)
store1.inventory()

#remove storwide brand sale
store1.remove_sale('Kate Spade')

#check the inventory again (Kate Spade items sale price should reflect n/a; Nine West sale still in effect)
store1.inventory()

#search for a particular brand
store1.search_brand('Michael Kors')