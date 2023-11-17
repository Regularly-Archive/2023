using Microsoft.VisualBasic;
using Newtonsoft.Json;

namespace EdgeTTSSharp;
public sealed class VoicesManager
{
    private static Lazy<VoicesManager> _lazy = new Lazy<VoicesManager>(() => new VoicesManager());

    /// <summary>
    /// 当前发音人列表
    /// </summary>
    private IList<Voice> _voices = new List<Voice>();

    /// <summary>
    /// 调用顺序标志
    /// </summary>
    protected bool _calledCreated = false;

    private VoicesManager() { }


    public static async Task<VoicesManager> CreateAsync()
    {
        var voiceManager = _lazy.Value;
        if (!voiceManager._calledCreated)
        {
            voiceManager._voices = await ListVoice();
            voiceManager._calledCreated = true;
        }

        return voiceManager;
    }

    private async static Task<IList<Voice>> ListVoice(CancellationToken token = default)
    {

        using (var client = new HttpClient())
        {
            using (var request = new HttpRequestMessage(HttpMethod.Get, Constants.VOICE_LIST))
            {
                request.Headers.Add("Accept", "application/json");
                request.Headers.Add("Authority", "speech.platform.bing.com");
                request.Headers.Add("Sec-CH-UA", @""" Not;A Brand"";v=""99"", ""Microsoft Edge"";v=""91"", ""Chromium"";v=""91""");
                request.Headers.Add("Sec-CH-UA-Mobile", "?0");
                request.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41");
                request.Headers.Add("Accept", "*/*");
                request.Headers.Add("Sec-Fetch-Site", "none");
                request.Headers.Add("Sec-Fetch-Mode", "cors");
                request.Headers.Add("Sec-Fetch-Dest", "empty");
                request.Headers.Add("Accept-Encoding", "gzip, deflate, br");
                request.Headers.Add("Accept-Language", "en-US,en;q=0.9");

                using (var response = await client.SendAsync(request, token))
                {
                    response.EnsureSuccessStatusCode();

                    var payload = await response.Content.ReadAsStringAsync();

                    var voices = JsonConvert.DeserializeObject<List<Voice>>(payload) ?? new();

                    return voices
                        .Select(it =>
                        {
                            it.Language = it.Locale.Split('-')[0];
                            return it;
                        })
                        .ToList();
                }
            }
        }
    }

    public IList<Voice> Find(Func<Voice,bool> predicate = null)
    {
        if (!_calledCreated)
            throw new Exception("VoicesManager.find() called before VoicesManager.create().");

        return predicate != null ? _voices.Where(x => predicate(x)).ToList(): _voices;
    }


    public class Voice
    {
        public string Name { get; set; }
        public string ShortName { get; set; }
        public string Gender { get; set; }
        public string Locale { get; set; }
        public string SuggestedCodec { get; set; }
        public string FriendlyName { get; set; }
        public string Status { get; set; }
        public string Language { get; set; }
    }
}


