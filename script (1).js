function analyzeEmail() {
    const emailText = document.getElementById("emailInput").value;

    fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email_text: emailText })
    })
    .then(response => response.json())
    .then(data => {

        document.getElementById("score").innerText = data.risk_score;
        document.getElementById("keywords").innerText =
            data.suspicious_keywords.length > 0
            ? data.suspicious_keywords.join(", ")
            : "None";

        let badge = document.getElementById("badge");
        badge.className = "risk-badge";

        if (data.risk_level === "High") {
            badge.classList.add("high");
        } else if (data.risk_level === "Medium") {
            badge.classList.add("medium");
        } else {
            badge.classList.add("low");
        }

        badge.innerText = data.risk_level + " Risk";
    });
}