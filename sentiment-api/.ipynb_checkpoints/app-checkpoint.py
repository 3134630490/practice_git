from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# 创建API实例
app = FastAPI(title="Sentiment Analysis API")

# 加载模型
with open("svm_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)

# 定义请求格式
class TextRequest(BaseModel):
    text: str

# 预测接口
@app.post("/predict")
def predict_sentiment(request: TextRequest):
    text = request.text
    
    # 转换格式
    processed_text = " ".join(text.split())
    
    # TF-IDF转换
    X = tfidf.transform([processed_text])
    
    # 预测
    prediction = model.predict(X)[0]
    
    return {
        "text": text,
        "sentiment": int(prediction)
    }