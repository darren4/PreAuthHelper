let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const recordButton = document.getElementById('recordButton');
const transcriptDiv = document.getElementById('transcript');

recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        // Start recording
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        mediaRecorder.start();
        isRecording = true;
        recordButton.classList.add('recording');
        recordButton.textContent = 'Stop';
    } else {
        // Stop recording
        mediaRecorder.stop();
        isRecording = false;
        recordButton.classList.remove('recording');
        recordButton.textContent = 'Record';
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob);
            try {
                const response = await fetch('/transcribe', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                transcriptDiv.textContent = data.transcript;
            } catch (error) {
                console.error('Error:', error);
                transcriptDiv.textContent = 'Error transcribing audio.';
            }
            audioChunks = [];
        };
    }
}); 