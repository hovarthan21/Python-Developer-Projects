const guessBtn = document.getElementById("guessBtn");
const restartBtn = document.getElementById("restartBtn");
const message = document.getElementById("message");
const attemptsText = document.getElementById("attempts");
const progress = document.getElementById("progress");
const popup = document.getElementById("popup");
const canvas = document.getElementById("confettiCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let confettiPieces = [];

function createConfetti() {
  confettiPieces = [];
  for (let i = 0; i < 150; i++) {
    confettiPieces.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height - canvas.height,
      r: Math.random() * 6 + 2,
      d: Math.random() * 0.5 + 0.5,
      color: `hsl(${Math.random() * 360}, 100%, 50%)`
    });
  }
}

function drawConfetti() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  confettiPieces.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.fill();
  });

  confettiPieces.forEach(p => {
    p.y += p.d * 5;
    if (p.y > canvas.height) {
      p.y = -10;
      p.x = Math.random() * canvas.width;
    }
  });

  requestAnimationFrame(drawConfetti);
}

guessBtn.addEventListener("click", () => {
  const userInput = document.getElementById("userInput").value;
  
  fetch("/guess", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ guess: userInput })
  })
  .then(res => res.json())
  .then(data => {
    message.textContent = data.message;
    attemptsText.textContent = "Attempts: " + data.attempts;
    progress.style.width = (data.attempts * 5) + "%";

    if (data.status === "win") {
      popup.style.display = "block";
      createConfetti();
      drawConfetti();
      setTimeout(() => {
        popup.style.display = "none";
      }, 3000);
    }
  });
});

restartBtn.addEventListener("click", () => {
  fetch("/restart", { method: "POST" })
  .then(res => res.json())
  .then(data => {
    message.textContent = data.message;
    attemptsText.textContent = "Attempts: 0";
    progress.style.width = "0%";
    document.getElementById("userInput").value = "";
    popup.style.display = "none";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });
});

document.getElementById("singleBtn").addEventListener("click", () => {
  fetch("/mode", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ mode: "single" })
  }).then(() => {
    document.getElementById("setNumberBox").style.display = "none";
  });
});

document.getElementById("twoBtn").addEventListener("click", () => {
  fetch("/mode", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ mode: "two" })
  }).then(() => {
    document.getElementById("setNumberBox").style.display = "block";
  });
});

document.getElementById("setNumberBtn").addEventListener("click", () => {
  const num = document.getElementById("setNumberInput").value;
  fetch("/set_number", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ number: num })
  }).then(res => res.json())
  .then(data => {
    message.textContent = data.message;
    document.getElementById("setNumberBox").style.display = "none";
  });
});

