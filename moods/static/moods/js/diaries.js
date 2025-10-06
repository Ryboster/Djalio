// form_script.js
var selected;

function deselectLog(dbId) {
    const log = document.querySelector(`[dbid="${CSS.escape(dbId)}"]`);
    if (log) {
        log.setAttribute("selected", "");
        log.style.backgroundColor = "";
        log.style.borderColor = "";
    }
}

function selectLog(dbId) {
    const log = document.querySelector(`[dbid="${CSS.escape(dbId)}"]`);
    if (!log) return;
    
    if (!log.getAttribute("selected") || log.getAttribute("selected") === "") {
        log.setAttribute("selected", "true"); 
        if (selected && selected.getAttribute("dbid") != dbId) { 
            deselectLog(selected.getAttribute("dbid")); 
        }
        selected = log;
    } else {
        deselectLog(dbId);
        selected = null;
    }
}

function addMoodToOptions(options, newMood) {
    var newOption = `<option value="${newMood}">${newMood}</option>`;
    options += newOption;
    return options;
}

function PopulateMoodsOptions(moodsOptionsObj)
{
    let allOptions = "";
    const allMoods = JSON.parse(document.getElementById('allMoods').textContent);
    for (const [key, value] of Object.entries(allMoods))
    {
        allOptions = addMoodToOptions(allOptions, key);
        moodsOptionsObj.innerHTML = allOptions;
    }
}

function toggleAddEntryForm() {
    const addEntryForm = document.getElementById("addEntryFormOverlay");
    if (addEntryForm.style.display == "") {
        addEntryForm.style.display = "none";
    } else {
        addEntryForm.style.display = "";
    }
}

function GetColorForMood(mood)
{
    const allMoods = JSON.parse(document.getElementById('allMoods').textContent);
    for (const [key, value] of Object.entries(allMoods))
    {
        if (mood == key) { return allMoods[key]["Color"]; }
    }
    return "white";
}

function QueryDeletionOfCategory(category_ID, category_Name)
{
    document.getElementById("removeCategoryFormOverlay").style.display = "flex";
    document.getElementById("categoryToRemoveInputField").value = category_ID;
    document.getElementById("categoryToRemoveDisplayInputField").value = category_Name;
}

function QueryDeletionOfActivity(activity_ID, category_ID, activity_name, category_name)
{
    document.getElementById("removeActivityFormOverlay").style.display = "flex";
    document.getElementById("activityToRemoveInputField").value = activity_ID;
    document.getElementById("activityCategoryInputFieldR").value = category_ID;
    document.getElementById("activityCategoryInputFieldRDisplay").value = category_name;
    document.getElementById("activityToRemoveInputFieldDisplay").value = activity_name;
}

function toggleEditCategoryForm(category_key)
{
    
    const allCategories = JSON.parse(document.getElementById("allCategories").textContent);
    

    document.getElementById('editCategoryFormOverlay').style.display = 'flex';
    document.getElementById("editCategoryFormHeader");
    document.getElementById("categoryNameToEditInputField").value = category_key;
    document.getElementById("categoryIDToEditInputField").value = allCategories[category_key]["Category_ID"];
}

function toggleMoodsView()
{
    document.getElementById("MoodsView").style.display = "flex";

    const allMoods = JSON.parse(document.getElementById("allMoods").textContent);
    const MoodsViewBackground = document.getElementById("MoodsViewBackground"); MoodsViewBackground.innerHTML = "";    
    const moodsList = document.createElement("ul");
    MoodsViewBackground.append(moodsList);

    for (const [key, val] of Object.entries(allMoods))
    {
        const moodPosition = document.createElement("div"); moodPosition.style = "display: flex; flex-direction: row; justify-content: space-between;";
        const moodCaption = document.createElement("span"); moodCaption.textContent = key;
        const moodButtons = document.createElement("div"); moodButtons.style = "display: flexl; flex-direction:row;"
        const removeMoodButton = document.createElement("button"); removeMoodButton.textContent = "x";
        removeMoodButton.onclick = () => {
            document.getElementById("removeMoodFormOverlay").style.display = "flex";
            document.getElementById("moodToRemoveDisplayInputField").value = key;
            document.getElementById("moodToRemoveInputField").value = allMoods[key]["Mood_ID"];
        }

        const editMoodButton = document.createElement("button"); editMoodButton.textContent = "Edit";
        editMoodButton.onclick = () => {
            document.getElementById("editMoodFormOverlay").style.display = "flex";
            document.getElementById("editMoodIDInputField").value = allMoods[key]["Mood_ID"];
            document.getElementById("editMoodPreviewNameInputField").value = key;
            document.getElementById("editMoodNameInputField").value = key;
            document.getElementById("editMoodScoreInputField").value = allMoods[key]["Score"];
            document.getElementById("editMoodColorInputField").value = allMoods[key]["Color"];
        }

        moodButtons.appendChild(editMoodButton);
        moodButtons.appendChild(removeMoodButton);
        moodPosition.appendChild(moodCaption);
        moodPosition.appendChild(moodButtons);
        moodsList.appendChild(moodPosition);
    }
    const addMoodButton = document.createElement("button"); addMoodButton.textContent = "+";
    addMoodButton.onclick = () => {
        document.getElementById("addMoodFormOverlay").style.display = "flex";
    }
    MoodsViewBackground.appendChild(addMoodButton);
}

function toggleAddCategoryForm()
{
    document.getElementById('addCategoryFormOverlay').style.display = 'flex';
    const allActivities = JSON.parse(document.getElementById("allActivities").textContent);
    const allCategories = JSON.parse(document.getElementById("allCategories").textContent);

    var existingCategoriesList = document.getElementById("existingCategoriesList");
    existingCategoriesList.innerHTML = "";

    for (const [key, value] of Object.entries(allCategories))
    {
        const existingCategoryContainer = document.createElement("div");
        existingCategoryContainer.className = "activityCategorySection";
        const existingCategoryCaption = document.createElement("p");
        const existingCategoryManagementPanel = document.createElement("div");
        const existingCategoryHeader = document.createElement("div");
        existingCategoryHeader.style.display = "flex;"
        existingCategoryHeader.style = "display: flex; justify-content: space-between;";
        existingCategoryHeader.appendChild(existingCategoryCaption);
        existingCategoryHeader.appendChild(existingCategoryManagementPanel);

        existingCategoryCaption.textContent = key;
        existingCategoryContainer.appendChild(existingCategoryHeader);
        existingCategoriesList.appendChild(existingCategoryContainer);
        existingCategoryContainer.appendChild(document.createElement("hr"));
        
        var editButton = document.createElement("button");
        var removeButton = document.createElement("button");
        const addActivityButton = document.createElement("button"); 
        addActivityButton.textContent = "+";
        addActivityButton.type = "button";
        addActivityButton.className = "addActivityBtn";
        addActivityButton.onclick = () => { 
            document.getElementById("addActivityFormOverlay").style.display = "flex";
            document.getElementById("activityCategoryInputField").value = allCategories[key]["Category_ID"];
        }
        editButton.type = "button";
        editButton.textContent = "Edit";
        editButton.onclick = () => {toggleEditCategoryForm(key);}
        removeButton.textContent = "X";
        removeButton.type = "button";
        removeButton.onclick = () => { QueryDeletionOfCategory(allCategories[key]["Category_ID"], key); }
        existingCategoryManagementPanel.appendChild(addActivityButton);
        existingCategoryManagementPanel.appendChild(editButton);
        existingCategoryManagementPanel.appendChild(removeButton);
        

        const activitiesUL = document.createElement("ul");
        activitiesUL.style.display = "grid";
        activitiesUL.style.gridTemplateColumns = "repeat(auto-fit, minmax(200px, 1fr))";
        activitiesUL.style = "display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; list-style: none; padding: 0; margin: 20px 0;"
        
        
        for (const [key1, value] of Object.entries(allActivities))
        {
            if (allActivities[key1]["Category_ID"] == allCategories[key]["Category_ID"])
            {
                const activityContainer = document.createElement("div");
                activityContainer.className = "activityContainer";
                const activityButtonsContainer = document.createElement("div");
                activityButtonsContainer.style = "display: flex; flex-direction: row; width: 35%;";
                const itemLabel = document.createElement("label"); 
                itemLabel.style = "width: 60%; overflow: scroll; font-size: 14px;"
                const editButton = document.createElement("button"); editButton.textContent = "Edit"; editButton.type = "button";
                const removeButton = document.createElement("button"); removeButton.textContent = "x"; removeButton.type = "button";
                removeButton.className = "removeActivityBtn";
                editButton.className = "editActivityBtn";

                removeButton.onclick = () => {
                    QueryDeletionOfActivity(allActivities[key1]["Activity_ID"], allActivities[key1]["Category_ID"], key1, key);
                }

                editButton.onclick = () => {
                    toggleEditActivityFormOverlay(key1, key);
                }

                activityButtonsContainer.appendChild(removeButton);
                activityButtonsContainer.appendChild(editButton);
                
                activityContainer.appendChild(itemLabel);
                activityContainer.appendChild(activityButtonsContainer);

                const listItem = document.createElement("li");
                listItem.className = "activityListItem";
                
                listItem.appendChild(activityContainer);
                itemLabel.innerHTML = key1;
                activitiesUL.appendChild(listItem);
            }
        }
        existingCategoryContainer.appendChild(activitiesUL);
    }
}

function toggleEditActivityFormOverlay(activity_name, category_name)
{
    document.getElementById("editActivityFormOverlay").style.display = "flex";
    const allCategories = JSON.parse(document.getElementById("allCategories").textContent);
    const allActivities = JSON.parse(document.getElementById("allActivities").textContent);

    var options = ``;
    for (const [key, val] of Object.entries(allCategories))
    {
        options += `<option value="${allCategories[key]["Category_ID"]}">${key}</option>`
    }
    document.getElementById("EditActivityCategoryInputField").innerHTML = options;
    
    document.getElementById("editActivityFormOverlay").style.display = "flex;";
    document.getElementById("EditActivityColorInputField").value = allActivities[activity_name]["Color"];
    document.getElementById("EditActivityIDInputField").value = allActivities[activity_name]["Activity_ID"];
    document.getElementById("EditActivityCategoryInputField").value = allCategories[category_name]["Category_ID"];
    document.getElementById("EditActivityNameDisplayInputField").value = activity_name;
    document.getElementById("EditActivityNewNameInputField").value = activity_name;
}

function populateEntries() {
    const allEntries = JSON.parse(document.getElementById("allEntries").textContent);
    const pageFeedList = document.getElementById("pageContentList");
    pageFeedList.innerHTML = "";

    for (const [key, value] of Object.entries(allEntries).sort((a, b) => b[0] - a[0]))
    {
            let entryActivities = allEntries[key]["Activities"];

            const postContainer = document.createElement("div"); 
            postContainer.className = "postContainer"; 
            postContainer.setAttribute("dbid", key);
            postContainer.onclick = () => selectLog(key);

            const dateContainer = document.createElement("div"); 
            dateContainer.className = "dateContainer";

            const moodContainer = document.createElement("div"); 
            const moodContent = document.createElement("span");
            moodContent.className = "moodContent";
            moodContent.style.backgroundColor = GetColorForMood(allEntries[key]["Mood"]);
            moodContainer.className = "moodContainer";

            const activitiesContainer = document.createElement("div"); 
            activitiesContainer.className = "activitiesContainer";

            const contentContainer = document.createElement("div"); 
            contentContainer.className = "contentContainer";

            dateContainer.textContent = allEntries[key]["Date"];
            moodContent.textContent = allEntries[key]["Mood"];

            activitiesContainer.innerHTML = "";
            activitiesContainer.style.display = "flex";
            activitiesContainer.style.flexWrap = "wrap";
            activitiesContainer.style.gap = "5px";

            if (!Array.isArray(entryActivities)) return;

            entryActivities.forEach(activity => {
                const activitySpan = document.createElement("span");
                activitySpan.className = "singleActivityBlock";
                activitySpan.textContent = activity;

                const allActivitiesData = JSON.parse(document.getElementById('allActivities').textContent);

                activitySpan.style.backgroundColor = allActivitiesData[activity]["Color"];
                activitiesContainer.appendChild(activitySpan);
            });

            contentContainer.innerHTML = allEntries[key]["Description"] || '';
            contentContainer.setAttribute('data-original-content', allEntries[key]["Description"]);
            postContainer.appendChild(dateContainer);
            moodContainer.appendChild(moodContent);
            postContainer.appendChild(moodContainer);
            postContainer.appendChild(activitiesContainer);
            postContainer.appendChild(contentContainer);
            pageFeedList.appendChild(postContainer);
    }
}

function populateEditEntryForm(selected) {
    if (!selected) return;
    
    const allActivities = JSON.parse(document.getElementById('allActivities').textContent);
    const allCategories = JSON.parse(document.getElementById("allCategories").textContent);
    
    document.getElementById("editFormActivitiesContainer").innerHTML = "";    
    document.getElementById("entryIDEditFormInputField").value = selected.getAttribute("dbid");
    PopulateMoodsOptions(document.getElementById("moodsEditFormInputField"));
    document.getElementById("moodsEditFormInputField").value = selected.querySelector('.moodContainer').textContent;
    
    const contentHTML = selected.querySelector('.contentContainer').getAttribute('data-original-content') || 
                       selected.querySelector('.contentContainer').textContent;
    document.getElementById("edit-content-input").value = contentHTML;
    
    // Get selected activities from the entry
    const activitiesContainer = selected.querySelector('.activitiesContainer');
    const selectedActivities = Array.from(activitiesContainer.children).map(child => 
        child.textContent.trim()
    );

    for (const [key, value] of Object.entries(allCategories))
    {
        const activityCategoryDivider = document.createElement("div");
        const activityHeaderDivider = document.createElement("div"); 
        activityHeaderDivider.style.display = "flex";
        const activityCategoryHeader = document.createElement("h3");
        activityCategoryHeader.textContent = key;
        const activitiesUL = document.createElement("ul");
        for (const [key1, value] of Object.entries(allActivities))
        {
            if (allActivities[key1]["Category_ID"] == allCategories[key]["Category_ID"])
            {
                activitiesUL

                const listItem = document.createElement("li");
                const itemLabel = document.createElement("label");
                const checkboxItem = document.createElement("input");
                checkboxItem.type = "checkbox";
                checkboxItem.value = key1;
                checkboxItem.name = "activities";
                
                if (selectedActivities.includes(key1)) {
                    checkboxItem.checked = true;
                }

                itemLabel.innerHTML = key1;
                listItem.appendChild(itemLabel);
                listItem.appendChild(checkboxItem);
                activitiesUL.appendChild(listItem);
            }
        }
        activityHeaderDivider.appendChild(activityCategoryHeader);
        activityCategoryDivider.appendChild(activityHeaderDivider);
        activityCategoryDivider.appendChild(activitiesUL);
        document.getElementById("editFormActivitiesContainer").appendChild(activityCategoryDivider);
    }
}

function PopulateAddEntryForm()
{
    document.getElementById("activitiesContainer").innerHTML = "";  
    
    const allCategories = JSON.parse(document.getElementById("allCategories").textContent);
    const moods = document.getElementById("moods");

    PopulateMoodsOptions(moods);

    for (const [activityCategoryName, value] of Object.entries(allCategories))
    {
        const activityCategoryDivider = document.createElement("div");
        activityCategoryDivider.className = "activityCategorySection";

        const activityHeaderDivider = document.createElement("div"); 
        activityHeaderDivider.className = "activityCategoryHeader";
        activityHeaderDivider.style.display = "flex";
        activityHeaderDivider.style.justifyContent = "space-between";
        activityHeaderDivider.style.alignItems = "center";
        
        const activityHeader = document.createElement("h3");
        activityHeader.textContent = activityCategoryName;
        
        // Create button container
        const buttonContainer = document.createElement("div");
        buttonContainer.className = "categoryButtonContainer";
        buttonContainer.style.display = "flex";
        buttonContainer.style.gap = "5px";
        
        const activitiesUL = document.createElement("ul");
        activitiesUL.className = "activitiesList";

        PopulateActivitiesForCategory(activitiesUL, allCategories[activityCategoryName]["Category_ID"], activityCategoryName);

        activityHeaderDivider.appendChild(activityHeader);
        activityHeaderDivider.appendChild(buttonContainer);
        activityCategoryDivider.appendChild(activityHeaderDivider);
        activityCategoryDivider.appendChild(activitiesUL);
        document.getElementById("activitiesContainer").appendChild(activityCategoryDivider);   
    }
}

function PopulateActivitiesForCategory(activitiesUL, category_ID, category_name)
{
    const allActivities = JSON.parse(document.getElementById('allActivities').textContent);
    for (const [activity, value] of Object.entries(allActivities))
        {
            if (allActivities[activity]["Category_ID"] == category_ID)
            {
                const listItem = document.createElement("li"); listItem.className = "activityListItem";
                const itemLabel = document.createElement("label");
                const checkboxItem = document.createElement("input");
                
                checkboxItem.type = "checkbox";
                checkboxItem.value = activity;
                checkboxItem.name = "activities";

                itemLabel.textContent = activity;
                listItem.appendChild(itemLabel);
                listItem.appendChild(checkboxItem);
                activitiesUL.appendChild(listItem);
            }
        }
}

function AddRemoveButton()
{
    const removeDiaryButton = document.createElement("button");
    removeDiaryButton.className = "removeDiaryButton";
    removeDiaryButton.style = "background: red; margin-top: auto;"
    removeDiaryButton.textContent = "Remove";
    removeDiaryButton.onclick = () => 
        {
            const confirmed = confirm("WARNING! You are about to remove this diary. This is irreversible. Do you want to continue?");
            if (confirmed) { window.location.href = "remove"; }
        }

    document.getElementById("filler").appendChild(removeDiaryButton);
}

// WHEN SITE CONTENT LOADED, RESPOND WITH: 
document.addEventListener("DOMContentLoaded", function () 
{
    console.log("document loaded");
    populateEntries();
    PopulateAddEntryForm();
    AddRemoveButton();
});