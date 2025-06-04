import os
import json
import wave
from vosk import Model, KaldiRecognizer

def transcrever_audio_vosk(audio_path, model_path, output_path=None):
    """
    Transcreve um arquivo de áudio usando o modelo Vosk.

    Args:
        audio_path (str): Caminho para o arquivo .wav.
        model_path (str): Caminho para o diretório do modelo Vosk descompactado.
        output_path (str): Caminho para salvar a transcrição (.txt ou .json). Opcional.

    Returns:
        dict: Transcrição completa com texto final e resultados por bloco.
    """
    # Carregar modelo
    model = Model(model_path)

    # Abrir áudio
    wf = wave.open(audio_path, "rb")
    assert wf.getnchannels() == 1
    assert wf.getsampwidth() == 2
    assert wf.getframerate() in [8000, 16000, 44100]

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    full_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res)
            full_text += res.get("text", "") + " "

    # Captura final
    final_res = json.loads(rec.FinalResult())
    results.append(final_res)
    full_text += final_res.get("text", "")

    # Resultado completo
    transcricao = {
        "texto_completo": full_text.strip(),
        "segmentos": results
    }

    # Salvar se necessário
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcricao, f, ensure_ascii=False, indent=2)

    return transcricao

# Exemplo de uso:
# model_dir = "/caminho/para/vosk-model-en-us-0.22"
# audio_file = "/caminho/para/audio.wav"
# output_file = "/caminho/para/transcricao.json"
# resultado = transcrever_audio_vosk(audio_file, model_dir, output_file)
