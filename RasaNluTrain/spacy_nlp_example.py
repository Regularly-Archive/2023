import spacy # 导包
# 加载模型
nlp = spacy.load("zh_core_web_md") 
# 使用模型，传入句子即可
doc = nlp("播放歌曲传奇")
# 获取分词结果
print([(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents])
