from client.api_methods import get_top_headlines, get_everything
import json
from mistralai.client import Mistral

api_key = "CGwRIIZFKIcnzjJIDvgeOcLuk2nTbHAL" #mistral api key
apikey = "925f63e18e8242a388d64c2b01e448c7" #newsapi.org

model = "mistral-medium-latest"
client = Mistral(api_key=api_key)

if __name__ == '__main__':
    q = input("тематика какая? ")
    kolvo = int(input("сколько новостей? "))
    js_res = get_everything(apikey, q=q, sort_by="publishedAt")

    with open('art.json', "w", encoding="utf-8") as f:
        json.dump(js_res, f, indent=4)

    articles = js_res["articles"][:kolvo]
    out = []
    all_texts = []
    for i, article in enumerate(articles):
        content = (article.get("content") or "").split("[+")[0].strip()
        text = "\n".join(filter(None, [
            article.get("title"),
            article.get("description"),
            content
        ]))
        if text:
            all_texts.append(f"Статья {i+1}:\n{text}")

    combined = "\n\n---\n\n".join(all_texts)
    response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Ты финансовый аналитик. Отвечай строго одним большим текстом"
            },
            {
                "role": "user",
                "content": (
                    f"""Ты — аналитик новостей.
                На основе списка новостей за последний день сделай аналитическую сводку
                на русском языке объемом 250-300 слов.

                Требования:
                - не перечисляй новости по отдельности
                - выдели ключевые события
                - объясни их значение
                - сделай общий вывод
                - строго по заданной тематике: {q}
                - всё в связный текст. Не перечисляй статьи по одной — пиши цельный аналитический обзор.

                Вот текст всех новостей: {combined}"""
                    )
                }
            ]
        )

    summary = response.choices[0].message.content.strip()
    

    with open('text.txt', "w", encoding="utf-8") as f:
        f.write(summary)
    print("done")

