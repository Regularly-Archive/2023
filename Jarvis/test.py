import os
from pocketsphinx import LiveSpeech, get_model_path

# keywords = ['jarvis', 'snowboy', 'hi']
# output_file = 'wakeup.keyphrase'

# # 使用 kws_plp 模块生成 wakeup.keyphrase 文件
# kws_plp(keyword_list=keywords, output_file=output_file)

# 设置 PocketSphinx 的语音唤醒模型和语音识别模型
model_path = get_model_path()
print('model_path:' + model_path)
wakeup_model = os.path.join(model_path, 'en-us/wakeup')
speech_model = os.path.join(model_path, 'en-us')

# 设置语音唤醒关键词
wakeup_keyword = 'hello'

# 创建 LiveSpeech 对象
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(speech_model, 'en-us'),
    lm=os.path.join(speech_model, 'en-us.lm.bin'),
    dic=os.path.join(speech_model, 'cmudict-en-us.dict'),
    # kws=os.path.join(wakeup_model, 'wakeup.keyphrase'),
    kws_threshold=1e-20
)

# 循环监听语音输入，当听到唤醒关键词时，输出提示信息
for phrase in speech:
    print(phrase)
    for item in phrase.segments(detailed=True):
        print(item)
    if wakeup_keyword in phrase.segments(detailed=True)[0][0]:
        print('Wake up!')