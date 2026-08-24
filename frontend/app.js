const API_BASE = "http://127.0.0.1:8000/api";

const jobForm = document.getElementById("jobForm");
const uploadForm = document.getElementById("uploadForm");
const jobSelect = document.getElementById("jobSelect");
const resultsArea = document.getElementById("resultsArea");
const uploadStatus = document.getElementById("uploadStatus");
const uploadBtn = document.getElementById("uploadBtn");
const refreshMatches = document.getElementById("refreshMatches");

async function loadJobs() {
    try {
        const response = await fetch(API_BASE + "/jobs/");
        const jobs = await response.json();
        
        jobSelect.innerHTML = '<option value="" disabled selected>Select a job...</option>';
        jobs.forEach(job => {
            const option = document.createElement("option");
            option.value = job.id;
            option.textContent = job.title;
            jobSelect.appendChild(option);
        });
    } catch (e) {
        console.error("Error loading jobs:", e);
        alert("Failed to load jobs. Is the backend running?");
    }
}

jobForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("jobTitle").value;
    const description = document.getElementById("jobDescription").value;

    try {
        const response = await fetch(API_BASE + "/jobs/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });
        if (response.ok) {
            alert("Job created!");
            jobForm.reset();
            loadJobs();
        }
    } catch (e) {
        alert("Error creating job: " + e);
    }
});

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const jobId = jobSelect.value;
    const fileInput = document.getElementById("resumeFile");
    
    if (!jobId || !fileInput.files[0]) {
        alert("Please select a job and a file.");
        return;
    }

    const formData = new FormData();
    formData.append("job_id", jobId);
    formData.append("file", fileInput.files[0]);

    uploadStatus.textContent = "Processing PDF and analyzing with LLM (this may take a few seconds)...";
    uploadStatus.classList.remove("hidden", "text-green-600", "text-red-600");
    uploadBtn.disabled = true;

    try {
        const response = await fetch(API_BASE + "/upload-resume/", {
            method: "POST",
            body: formData
        });
        
        const result = await response.json();
        if (response.ok) {
            uploadStatus.textContent = "Success! Score: " + result.score + "/10";
            uploadStatus.classList.add("text-green-600");
            loadMatches(jobId);
        } else {
            uploadStatus.textContent = "Error: " + result.detail;
            uploadStatus.classList.add("text-red-600");
        }
    } catch (e) {
        uploadStatus.textContent = "Error: " + e;
        uploadStatus.classList.add("text-red-600");
    } finally {
        uploadBtn.disabled = false;
        fileInput.value = "";
    }
});

async function loadMatches(jobId) {
    if (!jobId) return;
    
    try {
        const response = await fetch(API_BASE + "/matches/" + jobId);
        const matches = await response.json();
        
        resultsArea.innerHTML = "";
        
        if (matches.length === 0) {
            resultsArea.innerHTML = '<p class="text-gray-500 italic">No matches found for this job yet.</p>';
            return;
        }

        matches.forEach(match => {
            const card = document.createElement("div");
            card.className = "border rounded p-4 shadow-sm mb-4 bg-gray-50";
            
            const scoreColor = match.score >= 7 ? "text-green-600" : (match.score >= 4 ? "text-yellow-600" : "text-red-600");
            
            const skillsHtml = match.skills && match.skills.length > 0 
                ? match.skills.map(s => '<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">' + s + '</span>').join('') 
                : '<span class="text-xs text-gray-500">None extracted</span>';

            card.innerHTML = 
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-lg"> + match.filename + </h3>
                    <span class="font-bold text-xl  + scoreColor + "> + match.score + /10</span>
                </div>
                <div class="mb-2">
                    <span class="text-xs font-semibold uppercase text-gray-500">Justification:</span>
                    <p class="text-sm mt-1"> + match.justification + </p>
                </div>
                <div>
                    <span class="text-xs font-semibold uppercase text-gray-500">Extracted Skills:</span>
                    <div class="flex flex-wrap gap-1 mt-1">
                         + skillsHtml + 
                    </div>
                </div>
            ;
            resultsArea.appendChild(card);
        });
    } catch (e) {
        console.error("Error loading matches:", e);
    }
}

jobSelect.addEventListener("change", (e) => {
    loadMatches(e.target.value);
});

refreshMatches.addEventListener("click", () => {
    loadMatches(jobSelect.value);
});

loadJobs();
