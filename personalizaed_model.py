import openpyxl as oxl
import pulp as plp
import timeit

start = timeit.default_timer()

###### PROBLEM PARAMETERS

TARGET_LEVEL_7 = False
ONLY_USE_ADQUIRED_DRIVERS = True
MINIMUM_DRIVERS_PER_COURSE = 2
CONSIDER_CURRENT_INVESTMENT_LEVELS = True
REQUIRE_PRIORITY_DRIVERS = True
MINIMUM_PRIORITY_DRIVERS_PER_COURSE = 2
UNAQUIRED_DRIVERS_COST = 2 # Measured in tickets
PRIORITY_DRIVERS = ['Bowser (Santa)', 'Dry Bones (Gold)', 
'Gold Koopa (Freerunning)', 'King Bob-omb (Gold)', 'King Boo (Gold)',
'Mario (Hakama)', 'Mario (Tuxedo)', 'Pauline (Party Time)', 
'Peach (Vacation)', 'Pink Gold Peach', 'Rosalina (Swimwear)',
'Shy Guy (Ninja)', 'Mario (Sunshine)', 
'Boomerang Bro', 'Donkey Kong', 'Toad (Pit Crew)']

###### LOAD DATA

# Tickets and level
cost = {
'N':{'cost' : 800,
     'requirements' : {0:40 + UNAQUIRED_DRIVERS_COST, 1:40, 2:38, 3:33, 4:25, 5:14, 6:0, 7:20}
     },
'S':{'cost' : 3000,
     'requirements' : {0:15 + UNAQUIRED_DRIVERS_COST, 1:15, 2:14, 3:12, 4:9, 5:5, 6:0, 7:8}
     },
'H':{'cost' : 12000,
     'requirements' : {0:9 + UNAQUIRED_DRIVERS_COST, 1:9, 2:8, 3:7, 4:5, 5:3, 6:0, 7:5}
     }
}

wb = oxl.load_workbook('raw.xlsx')
ws = wb['base']

courses = set()
drivers = set()
coverage = {}
investment = {}
costs = {}

# Function that calculates a drivers cost to max out

def calculate_driver_cost(tier, driver, current_level, current_tickets):
    
    calculated_cost = 0
    
    if current_level < 6:    
        calculated_cost =  cost[tier]['cost'] * ( cost[tier]['requirements'][current_level] - current_tickets )
    
    calculated_cost +=  cost[tier]['cost'] * (cost[tier]['requirements'][7]) if TARGET_LEVEL_7 and current_level < 7 else 0

    if ( ONLY_USE_ADQUIRED_DRIVERS and current_level >= 1 ) or not ONLY_USE_ADQUIRED_DRIVERS :
        drivers.add(driver)
        costs[driver] = calculated_cost if CONSIDER_CURRENT_INVESTMENT_LEVELS else 1
        
    
# Load driver and iventory data    
        
row = 1
while( ws.cell(row=row, column=5).value is not None ):
    
    tier = ws.cell(row=row, column=4).value
    driver = ws.cell(row=row, column=5).value
    current_level = ws.cell(row=row, column=6).value
    current_tickets = ws.cell(row=row, column=7).value
    
    calculate_driver_cost(tier, driver, current_level, current_tickets)

    row += 1

# Read the course-driver coverage data

row = 1
while( ws.cell(row=row, column=1).value is not None ):
    
    driver = ws.cell(row=row, column=1).value.split(':')[0]
    course = ws.cell(row=row, column=2).value
    
    if str(course)[0] not in ('0', '^') and driver in drivers:
        
        if course in courses:
            coverage[course].add(driver)
        else:
            courses.add(course)
            coverage[course] = set([driver])
    
    row+= 1
    
# Remove unused priority drivers
prio_copy = set(PRIORITY_DRIVERS)
for d in prio_copy:
    if d not in drivers:
        PRIORITY_DRIVERS.remove(d)

# Minimum Drivers per Course
courses_copy = set(courses)
priority_courses = set()
for course in courses_copy:

    # Remove courses without the minimum required drivers
    if len(coverage[course]) < MINIMUM_DRIVERS_PER_COURSE:
        courses.remove(course)
        
    # Calculate if a course has enough priority drivers
    n = sum([ 1 if d in PRIORITY_DRIVERS else 0 for d in coverage[course] ])
    if n >= MINIMUM_PRIORITY_DRIVERS_PER_COURSE:
        priority_courses.add(course)


# Create the LP problem
model = plp.LpProblem('MKT_Maximum_Coverage', plp.LpMinimize)

variables = { (d,c) : plp.LpVariable(f'{d},{c}', lowBound=0, upBound=1, cat='Integer') for d in drivers for c in courses }
chosen_drivers = {d : plp.LpVariable(f'{d}', lowBound=0, upBound=1, cat='Integer') for d in drivers}

# objective function
model += plp.lpSum( costs[d] * chosen_drivers[d] for d in drivers )

# Constraint: Cover each course at least once
for c in courses:
    if not REQUIRE_PRIORITY_DRIVERS or c not in priority_courses:
        model += plp.lpSum( variables[d,c] for d in coverage[c] ) >= 1
    elif REQUIRE_PRIORITY_DRIVERS and c in priority_courses:
        model += plp.lpSum( variables[d,c] for d in PRIORITY_DRIVERS if d in coverage[c] ) >= 1
    
for d in drivers:
    model += 50 * chosen_drivers[d] >= plp.lpSum( variables[d,c] for c in courses ) 

# Solve the LP model
model.solve()
print( plp.LpStatus[model.status] )
print( plp.value(model.objective))

# Print the solution
OPTIMAL_DRIVERS = set()
for d in drivers:
    if chosen_drivers[d].varValue == 1 and costs[d] > 0:
        print(f'{d} requires {costs[d]} to max out')
        OPTIMAL_DRIVERS.add(d)

print(len(OPTIMAL_DRIVERS))

stop = timeit.default_timer()

print('Time: ', stop - start)  
