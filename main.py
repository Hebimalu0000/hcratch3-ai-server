from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# モデルとトークナイザーの初期化
CODE_MODEL_NAME = "Salesforce/codegen-350M-mono"  # コード生成用
CHAT_MODEL_NAME = "gpt2"                        # GPT-2を使用したチャットボット用

# コード生成モデルの初期化
code_tokenizer = AutoTokenizer.from_pretrained(CODE_MODEL_NAME)
code_model = AutoModelForCausalLM.from_pretrained(CODE_MODEL_NAME)

# GPT-2を使用したチャットパイプラインの初期化
chat_tokenizer = AutoTokenizer.from_pretrained(CHAT_MODEL_NAME)
chat_model = AutoModelForCausalLM.from_pretrained(CHAT_MODEL_NAME)

# FastAPIアプリの作成
app = FastAPI()

# リクエストボディの定義
class Request(BaseModel):
    task: str  # "codegen" または "chat"
    prompt: str
    max_length: int = 100
    conversation_id: str = None  # チャットの場合に会話IDを保持

# エンドポイント: コード生成とチャットボットの両方
@app.post("/process/")
async def process(request: Request):
    try:
        if request.task == "codegen":
            # コード生成処理
            inputs = code_tokenizer(request.prompt, return_tensors="pt")
            outputs = code_model.generate(inputs["input_ids"], max_length=request.max_length, num_return_sequences=1)
            generated_code = code_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return {"status": "success", "generated_code": generated_code}
        
        elif request.task == "chat":
            # チャットボット処理 (GPT-2)
            inputs = chat_tokenizer.encode(request.prompt, return_tensors="pt")
            outputs = chat_model.generate(inputs, max_length=request.max_length, num_return_sequences=1)

            # 応答をデコード
            response = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return {
                "status": "success",
                "response": response,
            }

        else:
            raise HTTPException(status_code=400, detail="Invalid task type. Use 'codegen' or 'chat'.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
