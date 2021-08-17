This script allows you to optimize top shelf coverage in Mario Kart tour. It models the problem as a set covering problem and find the global optima(s) through linear programming.

By adjusting the parameters on main.py you can:

* find the least ammount of drivers you need to have complete coverage 
* using your own inventory as input from the raw.xlsx file, find which drivers to invest into, to achieve maximum coverage while spending the least amount of tickets

Below you will find each parameter and its effect on the model:

TARGET_LEVEL_7: If set to True, the model will aim for level 7 drivers, otherwise it will aim for level 6.
HIGH_ENDS_ONLY: Self explanatory.
ONLY_USE_ADQUIRED_DRIVERS: Self explanatory. Note: It is recommended to leave this parameter set to False, even when optimizing your current inventory. This way, the model will tell you which drives you should try getting from future pipes / reruns, even if you don't currently own them.
MINIMUM_DRIVERS_PER_COURSE: This parameter only affects the model if ONLY_USE_ADQUIRED_DRIVERS is set to True. In that case, the model will only optimize for courses with at lesat n top shelf available drivers. i.e: if your only top shelf driver for RMX Vanilla Lake 1 is Toadette, but she doesnt give you any additional coverage other than this one map, it wouldnt make sense to invest in her and the model would ignore the map for its calculations. 
CONSIDER_CURRENT_INVESTMENT_LEVELS: Self Explanatory. If set to True the model will minimize the total amount of coins worth of tickets you would have to invest to have level 6 or 7 coverage in every course, given your current inventory. If set to False, the model will instead minimize the total number of drivers you need for complete coverage, regardless of their current investment in your account. 
REQUIRE_PRIORITY_DRIVERS: If set to False, all drivers are considered equal. If set to True, in any course where there are at least n PRIORITY_DRIVERS that are top shelf, it will be required that the curse is covered by at least one of them. i.e: Currently there are 73 courses with at least 2 coinbox, giant bannana or boomerang drivers in their top shelf. If this parameter is set to true, the model will require that every one of those curses is covered by a driver with those special skills.
MINIMUM_PRIORITY_DRIVERS_PER_COURSE: This parameter only affects the model if REQUIRE_PRIORITY_DRIVERS is set to true. See the description of REQUIRE_PRIORITY_DRIVERS. This parameter represents n in the above description. Recommended value is 3 for f2p, 2 for gold pass users and 1 for whales.  
UNAQUIRED_DRIVERS_COST: Measured in tickets, this parameter only affects the model if ONLY_USE_ADQUIRED_DRIVERS is set to False. The parameter represents the additional cost of adquiring a new driver. Recommended value is 2. i.e: I don't currently own Explorer Peach but the coverage she provides is so valuable for my inventory that the model still recommends me to adquire and max her out, even if it costs me more than maxing my level 2 Black Birdo. Higher values of this parameter discourage adquiring new drivers and lower values encourage it. It is recommended to set the value of this parameter between a minimum of 1 and a maximum of 3.
PRIORITY_DRIVERS: The default list of priority drivers cosist of High End and Super users of Coinbox, Giant Bannana and Boomerang, as these are the highest scoring items in the game. You are free to add or remove drivers from this list. For instance, you might want to add your double or tripple capped drivers to this list. 
['Bowser (Santa)', 'Dry Bones (Gold)', 
'Gold Koopa (Freerunning)', 'King Bob-omb (Gold)', 'King Boo (Gold)',
'Mario (Hakama)', 'Mario (Tuxedo)', 'Pauline (Party Time)',
'Peach (Vacation)', 'Pink Gold Peach', 'Rosalina (Swimwear)',
'Shy Guy (Ninja)', 'Mario (Sunshine)', 
'Boomerang Bro', 'Donkey Kong', 'Toad (Pit Crew)']
FIND_ALL_COMBINATIONS. Self Explanatory. Keep in mind that if this parameter is set to true the program might have a higher runtime.

