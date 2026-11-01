import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Lo Siento, Te Quiero Mucho",
    page_icon=":3",
    layout="centered"
)

# Integración del diseño CSS, animaciones y audio con Tone.js
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #fff0f3 0%, #ffccd5 50%, #ffb3c1 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
        }

        .font-romantic { font-family: 'Dancing Script', cursive; }

        @keyframes heartbeat {
            0% { transform: scale(1); }
            14% { transform: scale(1.12); }
            28% { transform: scale(1); }
            42% { transform: scale(1.12); }
            70% { transform: scale(1); }
        }
        .animate-heartbeat { animation: heartbeat 2s infinite ease-in-out; }

        .heart-particle {
            position: absolute;
            pointer-events: none;
            opacity: 0.7;
            animation: floatUp linear forwards;
        }

        @keyframes floatUp {
            0% { transform: translateY(100vh) scale(0.5) rotate(0deg); opacity: 0; }
            10% { opacity: 0.8; }
            90% { opacity: 0.8; }
            100% { transform: translateY(-10vh) scale(1.2) rotate(360deg); opacity: 0; }
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 20px 40px rgba(230, 57, 70, 0.15);
        }

        .rain-heart {
            position: fixed;
            top: -50px;
            pointer-events: none;
            z-index: 50;
            animation: fall linear forwards;
        }

        @keyframes fall {
            to { transform: translateY(105vh) rotate(360deg); }
        }
    </style>
</head>
<body>
    <div id="bg-hearts-container" class="fixed inset-0 pointer-events-none overflow-hidden z-0"></div>

    <main class="relative z-10 max-w-lg w-full glass-card rounded-3xl p-8 text-center my-4">
        <div class="relative inline-block mb-4">
            <div class="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto shadow-inner border-2 border-rose-200">
                <i class="fa-solid fa-heart text-5xl text-rose-500 animate-heartbeat"></i>
            </div>
        </div>

        <h1 class="font-romantic text-4xl sm:text-5xl text-rose-600 font-bold mb-3">
            Lo siento, te quiero mucho
        </h1>

        <p class="text-gray-700 text-base mb-6 font-light leading-relaxed">
            Eres lo más importante para mí. Perdóname, no me gusta estar mal contigo. 💕
        </p>

        <div class="space-y-3">
            <button onclick="triggerHeartRain()" class="w-full py-4 px-6 bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white font-semibold rounded-2xl shadow-lg shadow-rose-300 transition-all duration-300 transform hover:-translate-y-1 active:translate-y-0 flex items-center justify-center gap-2">
                <i class="fa-solid fa-heart-pulse"></i>
                <span>Abrazo virtual</span>
            </button>

            <button onclick="toggleAudio()" class="w-full py-3 px-6 bg-white/80 hover:bg-white text-rose-600 border border-rose-200 font-medium rounded-2xl shadow-sm transition-all duration-200 text-sm flex items-center justify-center gap-2">
                <i id="musicIcon" class="fa-solid fa-music"></i>
                <span id="musicText">Activar música</span>
            </button>
        </div>

        <div class="mt-8 pt-6 border-t border-rose-100 text-rose-400 text-sm font-medium">
            De: Isa &nbsp;|&nbsp; Para: Yordis
        </div>
    </main>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <script>
        const bgHeartsContainer = document.getElementById('bg-hearts-container');
        const colors = ['#ff4d6d', '#ff758f', '#ffb3c1', '#e63946', '#c9184a'];

        function createBgHeart() {
            const heart = document.createElement('i');
            heart.className = 'fa-solid fa-heart heart-particle';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.color = colors[Math.floor(Math.random() * colors.length)];
            heart.style.fontSize = `${Math.random() * 20 + 12}px`;
            const duration = Math.random() * 6 + 6;
            heart.style.animationDuration = `${duration}s`;
            bgHeartsContainer.appendChild(heart);
            setTimeout(() => heart.remove(), duration * 1000);
        }

        setInterval(createBgHeart, 400);

        function triggerHeartRain() {
            for (let i = 0; i < 40; i++) {
                setTimeout(() => {
                    const rainHeart = document.createElement('i');
                    rainHeart.className = 'fa-solid fa-heart rain-heart';
                    rainHeart.style.left = Math.random() * 100 + 'vw';
                    rainHeart.style.color = colors[Math.floor(Math.random() * colors.length)];
                    rainHeart.style.fontSize = `${Math.random() * 25 + 15}px`;
                    const duration = Math.random() * 2 + 2;
                    rainHeart.style.animationDuration = `${duration}s`;
                    document.body.appendChild(rainHeart);
                    setTimeout(() => rainHeart.remove(), duration * 1000);
                }, i * 60);
            }
            playChime();
        }

        let synth = null;
        let isPlaying = false;
        let loopSequence = null;

        function initAudio() {
            synth = new Tone.PolySynth(Tone.Synth, {
                oscillator: { type: 'sine' },
                envelope: { attack: 0.1, decay: 0.3, sustain: 0.4, release: 1.2 }
            }).toDestination();
            synth.volume.value = -12;
        }

        function toggleAudio() {
            if (!synth) initAudio();
            Tone.start();

            const musicText = document.getElementById('musicText');
            const musicIcon = document.getElementById('musicIcon');

            if (!isPlaying) {
                const notes = [
                    { time: '0:0', note: 'C4' }, { time: '0:2', note: 'E4' },
                    { time: '0:3', note: 'G4' }, { time: '1:0', note: 'B4' },
                    { time: '1:2', note: 'C5' }, { time: '2:0', note: 'A4' },
                    { time: '2:2', note: 'F4' }, { time: '3:0', note: 'G4' }
                ];
                loopSequence = new Tone.Part((time, value) => {
                    synth.triggerAttackRelease(value.note, '8n', time);
                }, notes);
                loopSequence.loop = true;
                loopSequence.loopEnd = '4m';
                Tone.Transport.bpm.value = 75;
                Tone.Transport.start();
                loopSequence.start(0);
                isPlaying = true;
                musicText.innerText = "Pausar música";
                musicIcon.className = "fa-solid fa-pause";
            } else {
                Tone.Transport.stop();
                if (loopSequence) loopSequence.stop();
                isPlaying = false;
                musicText.innerText = "Activar música";
                musicIcon.className = "fa-solid fa-music";
            }
        }

        function playChime() {
            if (!synth) initAudio();
            Tone.start();
            const now = Tone.now();
            synth.triggerAttackRelease("C5", "8n", now);
            synth.triggerAttackRelease("E5", "8n", now + 0.1);
            synth.triggerAttackRelease("G5", "8n", now + 0.2);
            synth.triggerAttackRelease("C6", "4n", now + 0.3);
        }
    </script>
</body>
</html>
"""

# Renderizar en la aplicación Streamlit
components.html(html_content, height=720, scrolling=False)
