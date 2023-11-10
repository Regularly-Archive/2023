import { VOICE_LIST } from "./constant"

const list_voices = function() {
    const data = fetch(VOICE_LIST,{
        mode: "cors",
        method: 'GET',
        credentials: 'include',
        headers: {
            "Authority": "speech.platform.bing.com",
            "Sec-CH-UA": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
            "Sec-CH-UA-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
            "Accept": "*/*",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
    })
    .then(res => res.json())
    .catch(error => console.error(error))

    return data
}

export class VoicesManager {
    static voices = []
    static called_create = false

    static create() {
        const voiceManager = new VoicesManager();
        voiceManager.voices = list_voices()
        for (let voice of voiceManager.voices) {
            voice['Language'] = voice['Locale'].split("-")[0]
        }
        voiceManager.called_create = true;
        return voiceManager
    }
    
    static find(selector) {
        if (!this.called_create) {
            throw new Error('VoicesManager.find() called before VoicesManager.create()')
        }

        const mached_voices = this.voices.filter(selector)
        return mached_voices
    }
}