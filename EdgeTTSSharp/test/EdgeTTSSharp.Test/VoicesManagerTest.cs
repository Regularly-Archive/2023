using Xunit;

namespace EdgeTTSSharp.Test;

public class VoicesManagerTest
{
    [Fact]
    public async Task Test_CreateShouldReturnsSingleton()
    {
        var voicesManager1 = await VoicesManager.CreateAsync();
        var voicesManager2 = await VoicesManager.CreateAsync();
        Assert.Equal(voicesManager1, voicesManager2);
    }

    [Fact]
    public async Task Test_ListVoices()
    {
        var voicesManager = await VoicesManager.CreateAsync();
        var voiceList = voicesManager.Find(null);
        Assert.True(voiceList.Count > 0);
    }

    [Fact]
    public async Task Test_FindVoice()
    {
        var voicesManager = await VoicesManager.CreateAsync();
        var voiceList = voicesManager.Find(v => v.Locale == "zh-CN");
        Assert.True(voiceList.Count > 0);
    }
}