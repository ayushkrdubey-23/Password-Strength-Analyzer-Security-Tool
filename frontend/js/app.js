"use strict";

const analyzerForm = document.getElementById("analyzerForm");
const generatorForm = document.getElementById("generatorForm");

const analysisPassword = document.getElementById("analysisPassword");
const toggleAnalysisPassword = document.getElementById(
    "toggleAnalysisPassword"
);

const analysisStatus = document.getElementById("analysisStatus");
const analysisResults = document.getElementById("analysisResults");

const scoreValue = document.getElementById("scoreValue");
const scoreBar = document.getElementById("scoreBar");
const scoreDescription = document.getElementById("scoreDescription");
const strengthBadge = document.getElementById("strengthBadge");

const findingsList = document.getElementById("findingsList");
const suggestionsList = document.getElementById("suggestionsList");

const metricLength = document.getElementById("metricLength");
const metricCharacters = document.getElementById("metricCharacters");
const metricRisks = document.getElementById("metricRisks");

const scoreChartCanvas = document.getElementById("scoreChart");

const passwordLength = document.getElementById("passwordLength");
const lengthValue = document.getElementById("lengthValue");

const generatorStatus = document.getElementById("generatorStatus");
const generatedResult = document.getElementById("generatedResult");
const generatedPassword = document.getElementById("generatedPassword");

const toggleGeneratedPassword = document.getElementById(
    "toggleGeneratedPassword"
);

const copyPasswordButton = document.getElementById("copyPassword");

let scoreChart = null;


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

    button.setAttribute(
        "aria-pressed",
        String(currentlyHidden)
    );
}


// Convert strength categories into CSS class names.
function getStrengthClass(strength) {
    return String(strength)
        .toLowerCase()
        .replaceAll(" ", "-");
}


// Return the number of enabled character categories.
function countCharacterTypes(characterTypes) {
    if (
        !characterTypes ||
        typeof characterTypes !== "object"
    ) {
        return 0;
    }

    const categories = [
        "lowercase",
        "uppercase",
        "digits",
        "symbols"
    ];

    return categories.filter(
        (category) => characterTypes[category] === true
    ).length;
}


// Count detected risk categories using actual analyzer results.
function countDetectedRisks(analyses) {
    if (!analyses || typeof analyses !== "object") {
        return 0;
    }

    const riskCategories = [
        "common_password",
        "sequences",
        "keyboard_patterns",
        "repetitions",
        "predictable_patterns"
    ];

    return riskCategories.filter(
        (category) => analyses[category]?.detected === true
    ).length;
}


// Choose an explanation for the educational score.
function getScoreDescription(strength) {
    const descriptions = {
        "VERY WEAK": "Several serious weaknesses were identified.",
        "WEAK": "This password needs significant improvement.",
        "MODERATE": "Some improvements can make it stronger.",
        "STRONG": "The analyzed password has good characteristics.",
        "VERY STRONG": "The analyzed password passed these local checks."
    };

    return descriptions[strength] ||
        "Educational password strength score.";
}


// Update the visual score chart.
function updateScoreChart(score) {
    if (
        typeof Chart === "undefined" ||
        !scoreChartCanvas
    ) {
        return;
    }

    if (scoreChart) {
        scoreChart.destroy();
        scoreChart = null;
    }

    const remainingScore = Math.max(0, 100 - score);

    scoreChart = new Chart(scoreChartCanvas, {
        type: "doughnut",

        data: {
            labels: [
                "Score",
                "Remaining"
            ],

            datasets: [
                {
                    data: [
                        score,
                        remainingScore
                    ],

                    backgroundColor: [
                        "#3157d5",
                        "#e1e7f1"
                    ],

                    borderWidth: 0,
                    hoverOffset: 4
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "76%",

            plugins: {
                legend: {
                    display: false
                },

                tooltip: {
                    callbacks: {
                        label(context) {
                            return `${context.label}: ${context.raw}`;
                        }
                    }
                }
            },

            animation: {
                duration: 500
            }
        }
    });
}


// Update the analysis metrics using backend results.
function updateMetrics(data) {
    const analyses = data.analyses || {};

    const lengthResult = analyses.length || {};
    const characterResult = analyses.characters || {};

    const length = Number.isFinite(lengthResult.length)
        ? lengthResult.length
        : 0;

    const characterCount = countCharacterTypes(
        characterResult.character_types
    );

    const detectedRisks = countDetectedRisks(analyses);

    metricLength.textContent = `${length} characters`;
    metricCharacters.textContent = `${characterCount} / 4`;
    metricRisks.textContent = `${detectedRisks} / 5`;
}


// Update the analysis results section.
function displayAnalysisResults(data) {
    const score = Math.max(
        0,
        Math.min(100, Number(data.score) || 0)
    );

    const strength = String(data.strength || "UNKNOWN");

    scoreValue.textContent = String(score);

    scoreBar.style.width = `${score}%`;
    scoreBar.setAttribute("aria-valuenow", String(score));

    strengthBadge.textContent = strength;
    strengthBadge.className =
        `strength-badge ${getStrengthClass(strength)}`;

    scoreDescription.textContent =
        getScoreDescription(strength);

    updateScoreChart(score);
    updateMetrics(data);

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

    if (!password) {
        showStatus(
            analysisStatus,
            "Enter a synthetic demo password first.",
            "error"
        );
        return;
    }

    analysisResults.classList.add("hidden");

    showStatus(
        analysisStatus,
        "Analyzing password...",
        "success"
    );

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

            body: JSON.stringify({
                password: password
            })
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
            error.message ||
                "Unable to connect to the analysis service.",
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

        toggleGeneratedPassword.setAttribute(
            "aria-label",
            "Show generated password"
        );

        toggleGeneratedPassword.setAttribute(
            "aria-pressed",
            "false"
        );

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