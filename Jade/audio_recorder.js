// audio_recorder.js
function audioRecorder(options) {
  let recorder;
  let audioChunks = [];

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };

    recorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);

      // Send the audio data to Streamlit (implementation depends on the Streamlit component API)
      options.onStop(audioBlob);

      audioChunks = [];
    };

    recorder.start();
  }

  function stopRecording() {
    recorder.stop();
  }

  return {
    startRecording: startRecording,
    stopRecording: stopRecording
  };
}