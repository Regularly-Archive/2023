using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static EdgeTTSSharp.VoicesManager;

namespace EdgeTTSSharp
{
    public class Constants
    {

        protected const string WSS_BASE_URL = "wss://speech.platform.bing.com/consumer/speech/synthesize";
        protected const string HTTPS_BASE_URL = "https://speech.platform.bing.com/consumer/speech/synthesize";
        protected const string TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4";

        /// <summary>
        /// WebSocket请求地址
        /// </summary>
        public const string WSS_URL = $"{WSS_BASE_URL}/readaloud/edge/v1?TrustedClientToken={TRUSTED_CLIENT_TOKEN}";

        /// <summary>
        /// 获取声音列表请求地址
        /// </summary>
        public const string VOICE_LIST = $"{HTTPS_BASE_URL}/readaloud/voices/list?trustedclienttoken={TRUSTED_CLIENT_TOKEN}";
    }
}
