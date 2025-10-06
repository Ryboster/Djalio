

document.addEventListener("DOMContentLoaded", function () 
{
    CreateNavbarContainers();
    PopulateNavbarContainers();
    CreateAddNewLogButton();
});

function PopulateNavbarContainers()
{
    const registry = JSON.parse(document.getElementById("registry").textContent);
    const navbar = document.getElementById("navbar");
    for (const catContainer of navbar.children)
    {
        const categoryContent = document.createElement("ul"); categoryContent.style = "list-style-type: none; display: none; flex-direction: column;";
        
        for (const [log_ID, val] of Object.entries(registry))
        {
            if (registry[log_ID]["Template"] == catContainer.textContent)
            {
                const diaryUrl = `/${registry[log_ID]["Template"]}/${log_ID}`;
                const aTag = document.createElement("a"); aTag.href = diaryUrl;
                aTag.style = "padding: 4px; margin-bottom: 3px; margin-top: 3px; text-align: left; display: inline-block; color: white; background-color: rgba(0,0,0, 0.2);"
                aTag.textContent = registry[log_ID]["Name"];
                categoryContent.appendChild(aTag);
            }
        } 
        catContainer.appendChild(categoryContent);   
    }
}

function CreateNavbarContainers()
{
    const navbar = document.getElementById("navbar");
    const registry = JSON.parse(document.getElementById("registry").textContent);
    var uniqueTemplates = [];

    for (const [log_ID, val] of Object.entries(registry))
    {
        if (!uniqueTemplates.includes(registry[log_ID]["Template"]))
        {
            uniqueTemplates.push(registry[log_ID]["Template"]);
        }
    }

    uniqueTemplates.forEach(templateName => {
        const catContainer = document.createElement("button"); catContainer.className = "collapsible"; catContainer.textContent = templateName;
        navbar.appendChild(catContainer);
        catContainer.onclick = function() {
            for (const child of this.children)
            {
                let current_display;
                if (child.style.display == "none") {current_display = "flex";}
                else {current_display = "none";}
                child.style.display = current_display;
            }
        }
    });
}

function CreateAddNewLogButton()
{
    const navbar = document.getElementById("navbar");
    const AddNewLogButton = document.createElement("button");
    AddNewLogButton.style = "margin-top: auto; text-align: center;";
    AddNewLogButton.textContent = "+";
    AddNewLogButton.onclick = () => {
        window.location.href = "/create_new/";
    }

    navbar.appendChild(AddNewLogButton);

}