
from Databases.CRUD import CRUD
import time
from django.shortcuts import render, redirect
from datetime import datetime
import os

class Diary(CRUD):
    def __init__(self):
        super().__init__()
        self.TEMPLATE_PAGE = "diaries.html"
        self.DIARY_DB_FILENAME = ""
        self.DIARY_ID = 0
        self.TEMPLATE_NAME = "Diary"

    def InitializeRenderObjects(self):
        self.contextDict = {}
        self.allMoodsDict = {}
        self.allActivitiesDict = {}
        self.allCategoriesDict = {}
        
    def GetDiaryFilename(self, diary_id):
        self.DIARY_DB_FILENAME = self.ReadDB("Registry", "All_Logs", "Filename", "Log_ID", diary_id)[0][0]

    ### Reads data from diary database, processes it, and sends it to frontend
    def RenderDiary(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        self.DIARY_ID = diary_id
        allMoods = self.ReadDB(self.DIARY_DB_FILENAME, "All_Moods")
        allActivities = self.ReadDB(self.DIARY_DB_FILENAME, "All_Activities")
        allCategories = self.ReadDB(self.DIARY_DB_FILENAME, "All_Categories")
        allEntries = self.ReadDB(self.DIARY_DB_FILENAME, "Entries")
        self.InitializeRenderObjects()

        ### Prepare Entries for frontend
        for record in allEntries:
            entry_ID = record[0]
            if entry_ID in self.contextDict.keys(): 
                continue
            if self.ReadDB(self.DIARY_DB_FILENAME, "Mood_Records", "Mood_ID", "Entry_ID", entry_ID) == None:
                continue

            activities = []
            mood_ID = self.ReadDB(self.DIARY_DB_FILENAME, "Mood_Records", "Mood_ID", "Entry_ID", entry_ID)[0][0]
            mood = self.ReadDB(self.DIARY_DB_FILENAME, "All_Moods", "Mood" ,"Mood_ID", mood_ID)[0][0]
            activity_IDs = self.ReadDB(self.DIARY_DB_FILENAME, "Activity_Records", "Activity_ID", "Entry_ID", entry_ID)
            for activity_ID_record in activity_IDs:
                activity_ID = activity_ID_record[0]
                activity = self.ReadDB(self.DIARY_DB_FILENAME, "All_Activities", "Activity", "Activity_ID", activity_ID)[0][0]
                activities.append(activity)
            self.contextDict[entry_ID] = {"Date": datetime.utcfromtimestamp(entry_ID).strftime('%Y-%m-%d %H:%M:%S'), "Description": record[1], "Mood": mood, "Activities": activities}

        ### Prepare Moods for frontend
        for record in allMoods:
            self.allMoodsDict[record[1]] = {}
            self.allMoodsDict[record[1]]["Mood_ID"] = record[0]
            self.allMoodsDict[record[1]]["Score"] = record[2]
            self.allMoodsDict[record[1]]["Color"] = record[3]

        ### Prepare Activities for frontend
        for record in allActivities:
            self.allActivitiesDict[record[2]] = {}
            self.allActivitiesDict[record[2]]["Color"] = record[3]
            self.allActivitiesDict[record[2]]["Category_ID"] = record[1]
            self.allActivitiesDict[record[2]]["Activity_ID"] = record[0]

        ### Prepare Categories for frontend
        for record in allCategories:
            self.allCategoriesDict[record[1]] = {}
            self.allCategoriesDict[record[1]]["Category_ID"] = record[0]

        self.contextDict = dict(sorted(self.contextDict.items()), reverse=True)
        context = {
            "registry": self.GetRegistry(),
            "allCategories": self.allCategoriesDict,
            "allMoods": self.allMoodsDict,
            "allEntries": self.contextDict,
            "allActivities": self.allActivitiesDict
        }
        
        return render(request, self.TEMPLATE_PAGE, context)


    def AddNewEntryToDiary(self, request, diary_id):
        if request.method != "POST":
            return redirect("/")
            
        self.GetDiaryFilename(diary_id)
        content = request.POST["content"]
        date = int(time.time())
        mood = None
        try:
            mood = request.POST["mood"]
        except KeyError:
            mood = None
        mood_ID = self.ReadDB(self.DIARY_DB_FILENAME, "All_Moods", "Mood_ID", "Mood", mood)[0][0]
        
        self.CreateInDB(self.DIARY_DB_FILENAME, "Entries", 
                   values=(date, content,), 
                   columns=("Entry_ID", "Description",))
        
        self.CreateInDB(self.DIARY_DB_FILENAME, "Mood_Records", 
                    values=(mood_ID, date,), 
                    columns=("Mood_ID, Entry_ID",))
        
        activities = request.POST.getlist("activities")
        for activity in activities:
            activity_ID = self.ReadDB(self.DIARY_DB_FILENAME, "All_Activities", "Activity_ID", "Activity", activity)[0][0]
            self.CreateInDB(self.DIARY_DB_FILENAME, "Activity_Records", 
                        values=(date, activity_ID,), 
                        columns=("Entry_ID", "Activity_ID",))
        return redirect(f"/{self.TEMPLATE_NAME}/{self.DIARY_ID}")

    def addNewMoodToDiary(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        score = request.POST["score"]
        mood = request.POST["mood"]
        color = request.POST.get("color", "#000000")  # Default color
        self.CreateInDB(self.DIARY_DB_FILENAME, "All_Moods", 
                   values=(score, mood, color), 
                   columns=("Score", "Mood", "Color"))
        return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def addNewCategory(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            categoryName = request.POST["categoryName"]
            self.CreateInDB(self.DIARY_DB_FILENAME, "All_Categories", 
                       values=(categoryName,), 
                       columns=("Category",))
            return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")
        
    def EditMood(self, request, diary_id):
        print(request.POST)
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            self.UpdateDB(self.DIARY_DB_FILENAME, 
                         "All_Moods",
                         columns=["Mood", "Score", "Color"],
                         whereColumn="Mood_ID",
                         whereValue=request.POST["Mood_ID"],
                         values=[request.POST["newMood"], request.POST["newScore"], request.POST["newColor"]])
        return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")
        
    def RemoveMood(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        print(request.POST)
        if request.method == "POST":
            self.DeleteInDB(self.DIARY_DB_FILENAME,
                            "All_Moods",
                            "Mood_ID",
                            request.POST["Mood_ID"]
                            )
        return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def addNewActivity(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            newActivity = request.POST["newActivity"]
            category_ID = request.POST["activityCategory"]
            color = request.POST.get("color", "#000000")  # Default color

            # Insert into activities table
            self.CreateInDB(self.DIARY_DB_FILENAME, "All_Activities", 
                       values=(newActivity, color, category_ID), 
                       columns=("Activity", "Color", "Category_ID"))
            return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def removeExistingActivity(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            activityToRemove = request.POST["activityToRemove"]
            self.DeleteInDB(self.DIARY_DB_FILENAME, "All_Activities", "Activity_ID", activityToRemove)
            return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def removeExistingEntry(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            print(f"trying to remove: {request.POST["entryToRemove"]}")
            self.DeleteInDB(self.DIARY_DB_FILENAME, "Entries",
                       whereColumn="Entry_ID", 
                       whereValue=request.POST["entryToRemove"])
            return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def editExistingEntry(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            entry_ID = request.POST["entryID"]
            mood = request.POST["mood"]
            content = request.POST["content"]
            activities = request.POST.getlist("activities")

            self.UpdateDB(self.DIARY_DB_FILENAME, "Entries",
                       columns=["Description"],
                       whereColumn="Entry_ID",
                       whereValue=entry_ID,
                       values=[content])

            mood_ID = self.ReadDB(self.DIARY_DB_FILENAME, "All_Moods", "Mood_ID", "Mood", mood)[0][0]
            self.UpdateDB(self.DIARY_DB_FILENAME, "Mood_Records",
                       columns=["Mood_ID"],
                       whereColumn="Entry_ID",
                       whereValue=entry_ID,
                       values=[mood_ID])

            self.DeleteInDB(self.DIARY_DB_FILENAME, "Activity_Records", "Entry_ID", entry_ID)

            for activity in activities:
                activity_ID = self.ReadDB(self.DIARY_DB_FILENAME, "All_Activities", "Activity_ID", "Activity", activity)[0][0]
                self.CreateInDB(self.DIARY_DB_FILENAME, "Activity_Records",
                            values=(entry_ID, activity_ID), 
                            columns=("Entry_ID", "Activity_ID"))

            return redirect(f"/Diary/{diary_id}")


    def removeExistingCategory(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            categoryToRemove = request.POST["categoryToRemove"]

            self.DeleteInDB(self.DIARY_DB_FILENAME, "All_Categories", 
                       whereColumn="Category_ID", 
                       whereValue=categoryToRemove)
            return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def editCategory(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            self.UpdateDB(self.DIARY_DB_FILENAME, "All_Categories",
                        columns=["Category"],
                        whereColumn="Category_ID",
                        whereValue=request.POST["categoryID"],
                        values=[request.POST["newCategoryName"]])

        return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")

    def editActivity(self, request, diary_id):
        self.GetDiaryFilename(diary_id)
        if request.method == "POST":
            self.UpdateDB(self.DIARY_DB_FILENAME, "All_Activities",
                        columns=["Activity", "Color", "Category_ID"],
                        whereColumn="Activity_ID",
                        whereValue=request.POST["ActivityID"],
                        values=[request.POST["newActivity"], request.POST["newColor"], request.POST["newCategoryID"]])
            return redirect(f"/{self.TEMPLATE_NAME}/{diary_id}")
        
    def RemoveDiary(self, request, diary_id):
        if request.method == "GET":
            self.DeleteInDB(self.REGISTRY_DB_FILENAME, "All_Logs", "Log_ID", diary_id)
            os.remove(os.path.join(self.DATABASES_ROOT_DIR, self.DIARY_DB_FILENAME) + self.DB_EXTENSION)
            request.session['registry'] = ""
            return redirect("/")