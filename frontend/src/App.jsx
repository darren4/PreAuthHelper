import React, { useRef, useState } from 'react';
import './App.css';

const STATUS = {
  idle: 'Start your clinical note.',
  recording: 'Listening…',
  processing: 'Processing request…',
  ready: 'Transcript ready. Review below.'
};

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [status, setStatus] = useState('idle');
  const [mode, setMode] = useState('simple');
  const [transcript, setTranscript] = useState('');
  const [editableTranscript, setEditableTranscript] = useState('');
  const [hasTranscript, setHasTranscript] = useState(false);
  const [genZMode, setGenZMode] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);

  const handleRecordClick = async () => {
    if (!isRecording) {
      setStatus('recording');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new window.MediaRecorder(stream);
      audioChunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      mediaRecorderRef.current.onstop = async () => {
        setStatus('processing');
        const audioBlob = new Blob(audioChunksRef.current, { type: 'mp3' });
        // Stop all tracks to release the mic
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
        }
        const formData = new FormData();
        formData.append('file', audioBlob, 'conversation_file.webm');
        try {
          const response = await fetch('http://localhost:5000/completeform', {
            method: 'POST',
            body: formData,
          });
          const data = await response.json();
          setTranscript(data.output);
          setEditableTranscript(data.output);
          setHasTranscript(true);
          setStatus('ready');
        } catch (error) {
          setTranscript('Error transcribing audio.');
          setEditableTranscript('Error transcribing audio.');
          setHasTranscript(true);
          setStatus('ready');
        }
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
      streamRef.current = stream;
    } else {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="App">
      <div className="top-bar">
        <div className="hamburger" tabIndex={0} aria-label="menu">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div className="top-controls">
          <div className="toggle">gen z mode
            <label className="switch">
              <input type="checkbox" checked={genZMode} onChange={() => setGenZMode(!genZMode)} />
              <span className="slider"></span>
            </label>
          </div>
          <span className="globe" title="Language">&#127760;</span>
        </div>
      </div>
      <div className="center-stack">
        <div className="status-label">{STATUS[status]}</div>
        <button
          id="recordButton"
          className={`record-button-teal${isRecording ? ' recording' : ''}`}
          aria-label={isRecording ? 'Stop recording' : 'Start recording'}
          onClick={handleRecordClick}
        >
          {/* No icon/text for minimalist look */}
        </button>
        {hasTranscript && (
          <div className="transcript-block">
            <textarea
              className="transcript-area"
              value={editableTranscript}
              onChange={e => setEditableTranscript(e.target.value)}
              rows={4}
            />
          </div>
        )}
      </div>
      <div className="bottom-controls">
        <div className="mode-toggle">
          <button className={`mode-btn${mode === 'simple' ? ' active' : ''}`} onClick={() => setMode('simple')}>Simple Note</button>
          <button className={`mode-btn${mode === 'structured' ? ' active' : ''}`} onClick={() => setMode('structured')}>Structured Form</button>
        </div>
        <button className="begin-btn">Begin Session</button>
      </div>
      <span className="info" title="Info">&#9432;</span>
    </div>
  );
}

export default App; 