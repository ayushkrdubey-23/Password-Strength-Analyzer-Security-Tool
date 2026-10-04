
"use strict";

const analyzerForm = document.getElementById("analyzerForm");
const generatorForm = document.getElementById("generatorForm");

const analysisPassword = document.getElementById("analysisPassword");
const toggleAnalysisPassword = document.getElementById("toggleAnalysisPassword");

const analysisStatus = document.getElementById("analysisStatus");
const analysisResults = document.getElementById("analysisResults");

const scoreValue = document.getElementById("scoreValue");
const scoreBar = document.getElementById("scoreBar");
const strengthBadge = document.getElementById("strengthBadge");

const findingsList = document.getElementById("findingsList");
const suggestionsList = document.getElementById("suggestionsList");

const passwordLength = document.getElementById("passwordLength");
const lengthValue = document.getElementById("lengthValue");

const generatorStatus = document.getElementById("generatorStatus");
const generatedResult = document.getElementById("generatedResult");
const generatedPassword = document.getElementById("generatedPassword");

const toggleGeneratedPassword = document.getElementById(
    "toggleGeneratedPassword"
);

const copyPasswordButton = document.getElementById("copyPassword");


// Display a status message without interpreting it as HTML.
function showStatus(element, message, type = "success") {
    element.textContent = message;
    element.className = `status-message status-${type}`;
}


// Populate a list safely using textContent.
function populateList(element, items, emptyMessage) {
    element.replaceChildren();

    const values = Array.isArray(items) ? items : [];

    if (values.length === 0) {
        const listItem = document.createElement("li");
        listItem.textContent = emptyMessage;
        element.appendChild(listItem);
        return;
    }

    values.forEach((item) => {
        const listItem = document.createElement("li");
        listItem.textContent = String(item);
        element.appendChild(listItem);
    });
}


// Change the visibility of a password field.
function togglePasswordVisibility(input, button) {
    const currentlyHidden = input.type === "password";

    input.type = currentlyHidden ? "text" : "password";
    button.textContent = currentlyHidden ? "Hide" : "Show";
    button.setAttribute(
        "aria-label",
        currentlyHidden ? "Hide password" : "Show password"
    );
}


// Convert strength categories into CSS class names.
function getStrengthClass(strength) {
    return String(strength)
        .toLowerCase()
        .replaceAll(" ", "-");
}


// Update the analysis results section.
function displayAnalysisResults(data) {
    scoreValue.textContent = String(data.score);
    scoreBar.style.width = `${data.score}%`;

    strengthBadge.textContent = data.strength;
    strengthBadge.className =
        `strength-badge ${getStrengthClass(data.strength)}`;

    populateList(
        findingsList,
        data.findings,
        "No specific weaknesses were detected by these checks."
    );

    populateList(
        suggestionsList,
        data.suggestions,
        "Continue following good password security practices."
    );

    analysisResults.classList.remove("hidden");
}


// Analyze a password using the Flask REST API.
analyzerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const password = analysisPassword.value;

    analysisResults.classList.add("hidden");
    showStatus(analysisStatus, "Analyzing password...", "success");

    const submitButton = analyzerForm.querySelector(
        'button[type="submit"]'
    );

    submitButton.disabled = true;

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ password })
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(
                result.error || "Password analysis failed."
            );
        }

        displayAnalysisResults(result.data);

        showStatus(
            analysisStatus,
            "Password analysis completed successfully.",
            "success"
        );

    } catch (error) {
        showStatus(
            analysisStatus,
            error.message || "Unable to connect to the analysis service.",
            "error"
        );

    } finally {
        submitButton.disabled = false;
    }
});


// Show or hide the analyzer input.
toggleAnalysisPassword.addEventListener("click", () => {
    togglePasswordVisibility(
        analysisPassword,
        toggleAnalysisPassword
    );
});


// Update the displayed password length.
passwordLength.addEventListener("input", () => {
    lengthValue.textContent = passwordLength.value;
});


// Generate a secure password using the Flask REST API.
generatorForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    generatedResult.classList.add("hidden");

    const submitButton = generatorForm.querySelector(
        'button[type="submit"]'
    );

    submitButton.disabled = true;

    const options = {
        length: Number(passwordLength.value),
        include_lowercase: document.getElementById(
            "includeLowercase"
        ).checked,
        include_uppercase: document.getElementById(
            "includeUppercase"
        ).checked,
        include_digits: document.getElementById(
            "includeDigits"
        ).checked,
        include_symbols: document.getElementById(
            "includeSymbols"
        ).checked
    };

    showStatus(
        generatorStatus,
        "Generating secure password...",
        "success"
    );

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(options)
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(
                result.error || "Password generation failed."
            );
        }

        generatedPassword.value = result.data.password;
        generatedPassword.type = "password";
        toggleGeneratedPassword.textContent = "Show";

        generatedResult.classList.remove("hidden");

        showStatus(
            generatorStatus,
            "Secure password generated successfully.",
            "success"
        );

    } catch (error) {
        showStatus(
            generatorStatus,
            error.message || "Unable to generate a password.",
            "error"
        );

    } finally {
        submitButton.disabled = false;
    }
});


// Show or hide the generated password.
toggleGeneratedPassword.addEventListener("click", () => {
    togglePasswordVisibility(
        generatedPassword,
        toggleGeneratedPassword
    );
});


// Copy the generated password only after a user action.
copyPasswordButton.addEventListener("click", async () => {
    const password = generatedPassword.value;

    if (!password) {
        showStatus(
            generatorStatus,
            "Generate a password before copying.",
            "error"
        );
        return;
    }

    try {
        await navigator.clipboard.writeText(password);

        showStatus(
            generatorStatus,
            "Generated password copied to clipboard.",
            "success"
        );

    } catch {
        showStatus(
            generatorStatus,
            "Clipboard access is unavailable in this browser.",
            "error"
        );
    }
});