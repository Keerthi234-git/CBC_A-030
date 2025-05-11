
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();
    recognition.onresult = function(event) {
        const userText = event.results[0][0].transcript;
        document.getElementById("userText").innerText = userText;
        fetch("/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text: userText})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("botResponse").innerText = data.response;
            speak(data.response);
        });
    };
}

function speak(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);
}

function getTherapistInfo() {
    fetch("/therapist", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({country: "India"})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("botResponse").innerText = data.info;
        speak(data.info);
    });
}
