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

function toggleAddEntryForm() {
    const addEntryForm = document.getElementById("addEntryFormOverlay");
    if (addEntryForm.style.display == "") {
        addEntryForm.style.display = "none";
    } else {
        addEntryForm.style.display = "";
    }
}

function populateEntries() {
    console.log("populating entries");
    const allEntries = JSON.parse(document.getElementById("availableEntries").textContent);
    console.log("Raw entries:", allEntries);

    const contentList = document.getElementById("pageContentList");
    contentList.innerHTML = ""; // Clear existing entries

    allEntries.forEach((entry, index) => {
        console.log("Processing entry:", entry);
        
        // Based on your database schema: ID, Date, Mood, Activities, Description
        // But the array might be: [Date, Mood, Activities, Description, ID]
        let date, mood, activities, content, dbID;
        
        if (Array.isArray(entry)) {
            if (entry.length === 5) {
                // Check which format we have by looking at the data
                // If first element looks like an ID (number), use: [ID, Date, Mood, Activities, Description]
                // If last element looks like an ID, use: [Date, Mood, Activities, Description, ID]
                
                if (typeof entry[0] === 'number' || (typeof entry[0] === 'string' && /^\d+$/.test(entry[0]))) {
                    // Format: [ID, Date, Mood, Activities, Description]
                    [dbID, date, mood, activities, content] = entry;
                } else {
                    // Format: [Date, Mood, Activities, Description, ID]
                    [date, mood, activities, content, dbID] = entry;
                }
            } else if (entry.length === 4) {
                // Missing ID, assume [Date, Mood, Activities, Description]
                [date, mood, activities, content] = entry;
                dbID = index + 1;
            }
        } else if (typeof entry === 'object') {
            // Object format
            date = entry.Date || entry.date;
            mood = entry.Mood || entry.mood;
            activities = entry.Activities || entry.activities;
            content = entry.Description || entry.description || entry.content;
            dbID = entry.ID || entry.id || index + 1;
        } else {
            console.error("Unknown entry format:", entry);
            return;
        }

        console.log("Extracted data:", { dbID, date, mood, activities, content });

        // Ensure dbID is clean
        dbID = String(dbID).replace(/[^a-zA-Z0-9_-]/g, '');
        if (!dbID) dbID = `entry_${index + 1}`;

        let parsedActivities = [];
        try {
            if (typeof activities === 'string') {
                // Handle different string formats
                if (activities.startsWith('[') && activities.endsWith(']')) {
                    // JSON array format
                    parsedActivities = JSON.parse(activities.replace(/'/g, '"'));
                } else {
                    // Single activity or comma-separated
                    parsedActivities = activities.split(',').map(a => a.trim()).filter(a => a);
                }
            } else if (Array.isArray(activities)) {
                parsedActivities = activities;
            }
        } catch (e) {
            console.error("Error parsing activities:", e, "Raw activities:", activities);
            parsedActivities = [];
        }

        const postContainer = document.createElement("div"); 
        postContainer.className = "postContainer"; 
        postContainer.setAttribute("dbid", dbID);
        postContainer.onclick = () => selectLog(dbID);

        const dateContainer = document.createElement("div"); 
        dateContainer.className = "dateContainer";
        
        const titleContainer = document.createElement("div"); 
        titleContainer.className = "titleContainer";
        
        const activitiesContainer = document.createElement("div"); 
        activitiesContainer.className = "activitiesContainer";
        
        const contentContainer = document.createElement("div"); 
        contentContainer.className = "contentContainer";

        // Set content in correct order
        dateContainer.textContent = date;
        titleContainer.textContent = mood;
        
        // Create activities with colors
        activitiesContainer.innerHTML = "";
        activitiesContainer.style.display = "flex";
        activitiesContainer.style.flexWrap = "wrap";
        activitiesContainer.style.gap = "5px";
        
        parsedActivities.forEach(activity => {
            const activitySpan = document.createElement("span");
            activitySpan.className = "singleActivityBlock";
            activitySpan.textContent = activity;
            
            // Find color for this activity
            const allActivitiesData = JSON.parse(document.getElementById('availableActivities').textContent);
            let activityColor = "#667eea"; // default color
            
            allActivitiesData.forEach(([categoryName, categoryActivities]) => {
                categoryActivities.forEach(categoryActivity => {
                    if (categoryActivity === activity) {
                        // You'll need to get the color from the activities table
                        // For now, using a default gradient
                        activityColor = "#667eea";
                    }
                });
            });
            
            activitySpan.style.backgroundColor = activityColor;
            activitiesContainer.appendChild(activitySpan);
        });
        
        contentContainer.innerHTML = content || '';
        

        // Store original content for editing
        contentContainer.setAttribute('data-original-content', content);

        // Append all elements
        postContainer.appendChild(dateContainer);
        postContainer.appendChild(titleContainer);
        postContainer.appendChild(activitiesContainer);
        postContainer.appendChild(contentContainer);

        contentList.appendChild(postContainer);
    });
}

function populateEditEntryForm(selected) {
    if (!selected) return;
    
    const allActivities = JSON.parse(document.getElementById('availableActivities').textContent);
    
    // Clear the edit form activities container first
    document.getElementById("editFormActivitiesContainer").innerHTML = "";
    
    // Populate form fields
    document.getElementById("entryIDEditFormInputField").value = selected.getAttribute("dbid");
    document.getElementById("entryDateEditFormInputField").value = selected.querySelector('.dateContainer').textContent;
    
    // Populate moods dropdown
    const availableMoods = JSON.parse(document.getElementById('availableMoods').textContent);
    let allOptions = "";
    availableMoods.forEach(moodOption => {
        allOptions = addMoodToOptions(allOptions, moodOption);
    });
    document.getElementById("moodsEditFormInputField").innerHTML = allOptions;
    document.getElementById("moodsEditFormInputField").value = selected.querySelector('.titleContainer').textContent;
    
    // Set content - get original HTML content
    const contentHTML = selected.querySelector('.contentContainer').getAttribute('data-original-content') || 
                       selected.querySelector('.contentContainer').textContent;
    document.getElementById("edit-content-input").value = contentHTML;
    
    // Get selected activities from the entry
    const activitiesContainer = selected.querySelector('.activitiesContainer');
    const selectedActivities = Array.from(activitiesContainer.children).map(child => 
        child.textContent.trim()
    );
    
    // Create activity checkboxes
    allActivities.forEach(([activityCategoryName, categoryActivitiesList]) => {
        const activityCategoryDivider = document.createElement("div");
        const activityHeaderDivider = document.createElement("div"); 
        activityHeaderDivider.style.display = "flex";
        const activityHeader = document.createElement("h3");
        activityHeader.textContent = activityCategoryName;
        const activitiesUL = document.createElement("ul");
        
        categoryActivitiesList.forEach(activity => {
            const listItem = document.createElement("li");
            const itemLabel = document.createElement("label");
            const checkboxItem = document.createElement("input");
            checkboxItem.type = "checkbox";
            checkboxItem.value = activity;
            checkboxItem.name = "activities";
            
            // Check if this activity was selected in the original entry
            if (selectedActivities.includes(activity)) {
                checkboxItem.checked = true;
            }
            
            itemLabel.innerHTML = activity;
            listItem.appendChild(itemLabel);
            listItem.appendChild(checkboxItem);
            activitiesUL.appendChild(listItem);
        });
        
        activityHeaderDivider.appendChild(activityHeader);
        activityCategoryDivider.appendChild(activityHeaderDivider);
        activityCategoryDivider.appendChild(activitiesUL);
        document.getElementById("editFormActivitiesContainer").appendChild(activityCategoryDivider);
    });
}

// Initialize page
populateEntries();

// WHEN SITE CONTENT LOADED, RESPOND WITH: 
document.addEventListener("DOMContentLoaded", function () {
    // Populate moods
    const availableMoods = JSON.parse(document.getElementById('availableMoods').textContent);
    const moods = document.getElementById("moods");
    let allOptions = "";
    availableMoods.forEach(moodOption => {
        allOptions = addMoodToOptions(allOptions, moodOption);
    });
    moods.innerHTML = allOptions;

    // Populate today's date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('todayDate').value = today;

    // Populate activities
    const allActivities = JSON.parse(document.getElementById('availableActivities').textContent);
    console.log("All activities:", allActivities);
    
    // Clear activities container first
    document.getElementById("activitiesContainer").innerHTML = "";
    
    allActivities.forEach(([activityCategoryName, categoryActivitiesList]) => {
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
        
        // Add activity button
        const addActivityButton = document.createElement("button"); 
        addActivityButton.textContent = "+";
        addActivityButton.type = "button";
        addActivityButton.className = "addActivityBtn";
        addActivityButton.onclick = () => { 
            document.getElementById("addActivityFormOverlay").style.display = "flex";
            document.getElementById("activityCategoryInputField").value = activityCategoryName;
        }
        
        // Remove category button
        const removeCategoryButton = document.createElement("button");
        removeCategoryButton.textContent = "Delete Category";
        removeCategoryButton.type = "button";
        removeCategoryButton.className = "deleteCategoryBtn";
        removeCategoryButton.onclick = () => {
            if (confirm(`Are you sure you want to delete the "${activityCategoryName}" category? This will also delete all activities in this category.`)) {
                document.getElementById("removeCategoryFormOverlay").style.display = "flex";
                document.getElementById("categoryToRemoveInputField").value = activityCategoryName;
            }
        }
        
        buttonContainer.appendChild(addActivityButton);
        buttonContainer.appendChild(removeCategoryButton);
        
        const activitiesUL = document.createElement("ul");
        activitiesUL.className = "activitiesList";

        categoryActivitiesList.forEach(activity => {
            const listItem = document.createElement("li");
            listItem.className = "activityListItem";
            
            const itemLabel = document.createElement("label");
            const checkboxItem = document.createElement("input");
            const removeActivityButton = document.createElement("button");
            
            checkboxItem.type = "checkbox";
            checkboxItem.value = activity;
            checkboxItem.name = "activities";
            
            removeActivityButton.textContent = "×"; 
            removeActivityButton.type = "button";
            removeActivityButton.className = "removeActivityBtn";
            removeActivityButton.onclick = () => {
                if (confirm(`Are you sure you want to delete the "${activity}" activity?`)) {
                    document.getElementById("removeActivityFormOverlay").style.display = "flex";
                    document.getElementById("activityToRemoveInputField").value = activity;
                    document.getElementById("activityCategoryInputFieldR").value = activityCategoryName;
                }
            }            

            itemLabel.textContent = activity;
            listItem.appendChild(removeActivityButton);
            listItem.appendChild(itemLabel);
            listItem.appendChild(checkboxItem);
            activitiesUL.appendChild(listItem);
        });

        activityHeaderDivider.appendChild(activityHeader);
        activityHeaderDivider.appendChild(buttonContainer);
        activityCategoryDivider.appendChild(activityHeaderDivider);
        activityCategoryDivider.appendChild(activitiesUL);
        document.getElementById("activitiesContainer").appendChild(activityCategoryDivider);
    });
});