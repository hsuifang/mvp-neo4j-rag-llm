# load prompt.txt
def load_prompt(prompt_path) -> str:
  """讀取 prompt .txt 檔案"""
  with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()
  return prompt