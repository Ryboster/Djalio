from django.shortcuts import render
import ast
from CRUD import CRUD
import json
from django.shortcuts import redirect

crud = CRUD()

def home(request):
    allEntries = crud.read("Entries", "entries")
    print(allEntries)
    allMoods = crud.read("Moods", "moods")
    allCategories = crud.read("Categories", "categories")
    allActivities = crud.read("Categories", "activities")
    
    sortedMoods = sortMoods(allMoods)
    
    # Group activities by category
    categorizedActivities = []
    for category in allCategories:
        categoryName = category[0]  # Category is the first column
        # Get activities for this category
        categoryActivities = [activity[0] for activity in allActivities if activity[2] == categoryName]  # activity[2] is Category column
        categorizedActivities.append((categoryName, categoryActivities))

    print("categorized activities")
    print(categorizedActivities)
    
    context = {
        "availableEntries": allEntries,
        "availableMoods": sortedMoods,
        "availableActivities": categorizedActivities,
    }
    return render(request, "home.html", context)

def sortMoods(allMoods):
    sortedMoodScores = sorted([x[0] for x in allMoods], reverse=True)
    sortedMoods = []
    for score in sortedMoodScores:
        for scoreMoodPair in allMoods:
            if scoreMoodPair[0] == score: 
                sortedMoods.append(scoreMoodPair[1])
    return sortedMoods

def addNewEntry(request):
    if request.method == "POST":
        date = request.POST["date"]
        mood = request.POST["mood"]
        content = request.POST["content"]
        activities = request.POST.getlist("activities")
        crud.create("Entries", "entries", 
                   values=(date, mood, str(activities), content), 
                   columns=("Date", "Mood", "Activities", "Description"))
        return redirect("/")

def addNewMood(request):
    if request.method == "POST":
        score = request.POST["score"]
        mood = request.POST["mood"]
        color = request.POST.get("color", "#000000")  # Default color
        crud.create("Moods", "moods", 
                   values=(score, mood, color), 
                   columns=("Score", "Mood", "Color"))
        return redirect("/")

def addNewCategory(request):
    if request.method == "POST":
        categoryName = request.POST["categoryName"]
        crud.create("Categories", "categories", 
                   values=(categoryName,), 
                   columns=("Category",))
        return redirect("/")

def addNewActivity(request):
    if request.method == "POST":
        activityName = request.POST["newActivity"]
        categoryName = request.POST["activityCategory"]
        color = request.POST.get("color", "#000000")  # Default color
        
        # Insert into activities table
        crud.create("Categories", "activities", 
                   values=(activityName, color, categoryName), 
                   columns=("Activity", "Color", "Category"))
        return redirect("/")

def removeExistingActivity(request):
    if request.method == "POST":
        activityToRemove = request.POST["activityToRemove"]
        categoryName = request.POST["activityCategory"]
        
        # Delete from activities table
        # Note: You might need to add a method to delete with multiple conditions
        # For now, assuming activity names are unique within a category
        allActivities = crud.read("Categories", "activities")
        for activity in allActivities:
            if activity[0] == activityToRemove and activity[2] == categoryName:
                # You'll need to add a way to identify the specific record
                # Since activities table doesn't have an ID, we'll delete by activity name
                crud.delete("Categories", "activities", 
                           whereColumn="Activity", 
                           whereValue=activityToRemove)
                break
        return redirect("/")

def removeExistingEntry(request):
    if request.method == "POST":
        crud.delete("Entries", "entries", 
                   whereColumn="ID", 
                   whereValue=request.POST["entryToRemove"])
        return redirect("/")

def editExistingEntry(request):
    if request.method == "POST":
        entryID = request.POST["entryID"]
        mood = request.POST["mood"]
        content = request.POST["content"]
        activities = request.POST.getlist("activities")
        
        crud.update("Entries", "entries",
                   columns=["Mood", "Activities", "Description"],
                   whereColumn="ID",
                   whereValue=entryID,
                   values=[mood, str(activities), content])
        return redirect("/")
    

def removeExistingCategory(request):
    if request.method == "POST":
        categoryToRemove = request.POST["categoryToRemove"]
        
        # Delete the category (activities will be deleted automatically due to CASCADE)
        crud.delete("Categories", "categories", 
                   whereColumn="Category", 
                   whereValue=categoryToRemove)
        return redirect("/")