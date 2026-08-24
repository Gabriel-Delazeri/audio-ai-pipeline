from domain.ports.transcription_service import TranscriptionService


class WhisperTranscriptionService(TranscriptionService):
    def __init__(self, model=None, model_name: str = "base"):
        self._model = model
        self._model_name = model_name

    def _get_model(self):
        if self._model is None:
            import whisper

            self._model = whisper.load_model(self._model_name)
        return self._model

    def transcribe(self, audio_path: str) -> str:
        model = self._get_model()
        result = model.transcribe(audio_path)
        return result["text"].strip()
