'''Sample random Scheduling problem.'''

import copy
import random

##########################################################################
# This section contains the base classes
##########################################################################

# Scramble up some random specs
NumberClasses = random.randint(40, 80)
NumberProfessors = random.randint(30, 50)
NumberRooms = random.randint(15, 20)
NumberStudents = random.randint(300, 600)
NumberTimeSlots = random.randint(9, 12)

# Print out configuration randomly-generated "constants"
print("Classes = %d" % NumberClasses)
print("Professors = %d" % NumberProfessors)
print("Rooms = %d" % NumberRooms)
print("Students = %d" % NumberStudents)
print("TimeSlots = %d" % NumberTimeSlots)
print()

# One instance per soom
class Room:
  def __init__(self, n):
    self.name = "B-%3.3d" % (100+n)
    self.size = 10 * random.randint(4, 10)
    
# One instance per class, which has 1 room, 1 timeSlot, 1 professor and many students
class Class:
  def __init__(self, n):
    self.name = "CS %3.3d" % (100+n)
    self.professor = None
    self.students = []
    
  def setProfessor(self, prof):
    self.professor = prof
  
  def setRoom(self, room):
    self.room = room
    
  def setTimeSlot(self, timeSlot):
    self.timeSlot = timeSlot
    
# One instance per professor who can teach many classes
class Professor:
  def __init__(self, n):
    self.name = "Dr. X%2.2d" % (n+1)
    
# One instance per student
class Student:
  def __init__(self, n):
    self.name = "student %3.3d" % n
    
  def addClass(self, cls):
    cls.students.append(self)
    
# Define all the object classes
class TimeSlot:
  def __init__(self, n):
    self.name = "time slot %2.2d" % n
    self.hour = "%2d:00" % (n+8)

# These must be the same for all schedules
Rooms = [Room(x) for x in range(0, NumberRooms)]
Professors = [Professor(x) for x in range(0, NumberProfessors)]
Students = [Student(x) for x in range(0, NumberStudents)]
TimeSlots = [TimeSlot(x) for x in range(0, NumberTimeSlots)]
BaseClasses = [Class(x) for x in range(0, NumberClasses)]

# Randomly assign students to classes. These do NOT change with each schedule.
for student in Students:
  for x in range(0, random.randint(3, 4)):
    cls = random.randint(0, NumberClasses-1)
    student.addClass(BaseClasses[cls])

# Generate some random data, giving each class a professor, a room and a time slot
class Schedule:
  def __init__(self):
    self.Classes = copy.deepcopy(BaseClasses)
    self.fitness = 0
    
    # Randomly assign professors, rooms and time slots to classes
    for cls in self.Classes:
      prof = random.randint(0, NumberProfessors-1)
      cls.setProfessor(Professors[prof])
      room = random.randint(0, NumberRooms-1)
      cls.setRoom(Rooms[room])
      timeSlot = random.randint(0, NumberTimeSlots-1)
      cls.setTimeSlot(TimeSlots[timeSlot])
      
##########################################################################
# This section is just for printing
##########################################################################

# Print the current schedule, by time slot
def printTimeSlots(schedule):
  print("%-5s %5s   %-10s %-10s %-10s %8s   %s" % (
      "Room", "Size", "Time", "Class", "Professor", "Students", "Error(s)"))
  for room in Rooms:
    for timeSlot in TimeSlots:
      dup = False
      for cls in schedule.Classes:
        if cls.room == room and cls.timeSlot == timeSlot:
          msg = ""
          if len(cls.students) > room.size: 
              msg += " *Overflow*"    
              schedule.fitness = schedule.fitness + 1
          if dup: 
              msg += " *Duplicate*" 
              schedule.fitness = schedule.fitness + 1
          print("%-5s %5d   %-10s %-10s %-10s %8d  %s" % (
              room.name,
              room.size,
              timeSlot.hour,
              cls.name,
              cls.professor.name,
              len(cls.students),
              msg))
              
          dup = True
              
# Show schedule for each professor
def printProfessors(schedule):
  line = "%-10s" % "Professor"
  for timeSlot in TimeSlots:
    line += "%8s" % timeSlot.hour
  print(line)

  for prof in Professors:
    line = "%-10s" % prof.name
    for timeSlot in TimeSlots:
      room = None
      for cls in schedule.Classes:
        if cls.professor == prof and cls.timeSlot == timeSlot:
          if room == None:
            room = cls.room.name
          else:
            room = "*ERR*"
            schedule.fitness = schedule.fitness + 1
      if room == None:
        line += "%8s" % "-  "
      else:
        line += "%8s" % room
    print(line)

##########################################################################
# This is the important section. It creates and prints a random schedule
# Your work starts here. For each class, you can ONLY change three values:
# professor, time slot and room. Everything else stays constant.
#
# Step 1: Select based on Fitness function
#     Based on NumberSchedules, select that many new pairs of schedules and rank
#     them. Fewer *Duplicate* *Overflow* and *ERR* is better. Look very carefully
#     at the Schedule() constructor (__init__).
#
# Step 2: Cross-over
#      Generate new Schedules by taking some # of classes from each "parent"
#
# Step 3: Mutate
#      Randomly change a professor, a room or a time slot on each new schedule.
#
##########################################################################

# For you to compute. Look at printTimeSlots() and printProfessors().
def fitness(schedule):
  return schedule.fitness
  
NumberSchedules = 5
schedules = [Schedule() for x in range(0, NumberSchedules)]
schedules =  sorted(schedules)

for schedule in schedules:
  print("=========================================================================")
  printTimeSlots(schedule)
  print()
  printProfessors(schedule)
  print()
  print("Fitness = %.5f" % fitness(schedule))
  print()
