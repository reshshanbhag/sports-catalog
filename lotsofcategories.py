from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///itemscatalogwithusersandtime.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category 1
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(name="SoccerCleats", description="Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface.", category=category1) 
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Shinguards", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Jersey", description="To soccer legend Diego Maradona of Argentina, giving everything for the shirt is a player's motto. In other words, the soccer jersey is everything a team stands for.",category=category1)
session.add(categoryItem3)
session.commit()

# Category 2
category2 = Category(name="Basketball")
session.add(category2)
session.commit()

categoryItem1 = CategoryItem(name="Backboard", description="A backboard is a piece of basketball equipment. It is a raised vertical board with an attached basket consisting of a net suspended from a hoop", category=category2)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Basketball Shoes", description="With constant jumping, starting and stopping, basketball shoes are designed to act as shock absorbers and provide ankle stability with the flexibility to allow players to move laterally.",category=category2)
session.add(categoryItem2)
session.commit()
                              

# Category 3
category3 = Category(name="Baseball")
session.add(category3)
session.commit()

categoryItem1 = CategoryItem(name="Baseball Bat", description="A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher.", category=category3)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Baseball", description="A baseball is a ball used in the sport of the same name, baseball. It is between 9 inches and 23.5 cm in circumference (around).", category=category3)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Baseball Gloves", description="A baseball glove, also known as a mitt, is the piece of equipment baseball players use while on defense.", category=category3)
session.add(categoryItem3)
session.commit()


# Category 4
category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

categoryItem1 = CategoryItem(name="Flying Disc", description="A concave plastic disk designed for skimming through the air as an outdoor game or amusement.", category=category4)
session.add(categoryItem1)
session.commit()


# Category 5
category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

categoryItem1 = CategoryItem(name="Goggles", description="Anti-fog products can be used on lower-end goggles without a coating or on old goggles that are starting to fog.", category=category5)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Snowboard", description="Snowboards are boards where both feet are secured to the same board, which are wider than skis, with the ability to glide on snow.", category=category5)
session.add(categoryItem2)
session.commit()


# Category 6
category6 = Category(name="RockClimbing")
session.add(category6)
session.commit()

categoryItem1 = CategoryItem(name="Anchor", description="a natural or artificial structure that holds the rope used for belaying in position", category=category6)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Belay", description="a rope setup worked by a climbers partner to catch the climber when he falls or lower him down after he finishes his ascent", category=category6)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Bolt", description="a permanent form of protection that is drilled into a rock, to which carabiners can attach", category=category6)
session.add(categoryItem3)
session.commit()


# Category 7
category7 = Category(name="Tennis")
session.add(category7)
session.commit()

categoryItem1 = CategoryItem(name="Rackets", description="A racket or racquet is a sports implement consisting of a handled frame with an open hoop across which a network of strings or catgut is stretched tightly. ", category=category7)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Tennis Ball", description="A tennis ball is a ball designed for the sport of tennis. Tennis balls are fluorescent yellow at major sporting events, but in recreational play can be virtually any color. ", category=category7)
session.add(categoryItem2)
session.commit()


# Category 8
category8 = Category(name="Skating")
session.add(category8)
session.commit()

categoryItem1 = CategoryItem(name="Roller Skates", description="each of a pair of boots, or metal frames attached to shoes, with four or more small wheels, for gliding across a hard surface.", category=category8)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Ice Skates", description="a boot with a blade attached to the bottom, used for skating on ice.", category=category8)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Skateboard", description=" a type of sports equipment used primarily for the sport of skateboarding. It usually consists of a specially designed maplewood board combined with a polyurethane coating used for making smoother slides and stronger durability.", category=category8)
session.add(categoryItem3)
session.commit()

# Category 9
category9 = Category(name="Hockey")
session.add(category9)
session.commit()

categoryItem1 = CategoryItem(name="HockeyStick", description="a long, thin implement with a curved end, used to hit or direct the puck or ball in ice hockey or field hockey.", category=category9)
session.add(categoryItem1)
session.commit()
                             
categoryItem2 = CategoryItem(name="Helmets", description="a long, thin implement with a curved end, used to hit or direct the puck or ball in ice hockey or field hockey.", category=category9)
session.add(categoryItem2)
session.commit()



print "added menu items!"
