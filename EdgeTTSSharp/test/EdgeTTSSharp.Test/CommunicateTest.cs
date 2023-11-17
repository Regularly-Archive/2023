using Newtonsoft.Json;
using Xunit;

namespace EdgeTTSSharp.Test;

public class CommunicateTest
{
    [Fact]
    public async Task Test_Communicate_Stream()
    {
        var voicesManager = await VoicesManager.CreateAsync();
        var voices = voicesManager.Find(v => v.Locale == "zh-CN" && v.Gender == "Male");

        var communicate = new Communicate(voices.FirstOrDefault(), rate: -25);
        using (var stream = File.Create("output.mp3"))
        {
            await communicate.Stream((result) =>
            {
                if (result.Type == "audio")
                    result.Data?.CopyTo(stream);

                if (result.Type == "WordBoundary")
                    Console.WriteLine(JsonConvert.SerializeObject(result));
            });
        }
    }

    [Fact]
    public void Test_Communicate_Save()
    { 
    } 
}

