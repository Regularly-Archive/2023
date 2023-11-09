
const WSS_BASE_URL = 'wss://speech.platform.bing.com/consumer/speech/synthesize'
const HTTPS_BASE_URL = 'https://speech.platform.bing.com/consumer/speech/synthesize'

export const TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"
export const WSS_URL = `${WSS_BASE_URL}/readaloud/edge/v1?TrustedClientToken=${TRUSTED_CLIENT_TOKEN}`
export const VOICE_LIST = `${HTTPS_BASE_URL}/readaloud/voices/list?trustedclienttoken=${TRUSTED_CLIENT_TOKEN}`
