# ============================================================
# app.py — الكود الرئيسي لتطبيق Flask
# ============================================================

from flask import Flask, render_template, request, url_for, redirect, session
from dotenv import load_dotenv
import json
import os

#  استيراد الكلاسات من الملف الجديد
from models import Exhibit, ExhibitBot


# ============================================================
#  تهيئة التطبيق
# ============================================================
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")


# ============================================================
#  تحميل بيانات المعروضات
# ============================================================
with open("data/exhibits.json", "r", encoding="utf-8") as f:
    data = json.load(f)

EXHIBITS = [
    Exhibit(
        _id=item['id'],
         name=item['name'],
         category=item['category'],
         image=item['image'],
         period=item['period'],
         origin=item['origin'],
         description=item['description']
    )
    for item in data
]

for ex in EXHIBITS:
    ex.bot = ExhibitBot(ex)

CATEGORIES = sorted(set(ex.category for ex in EXHIBITS))
ITEMS_PER_PAGE = 10


# ============================================================
#  الصفحة الرئيسية
# ============================================================
@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("question", "").strip()
    selected_category = request.args.get("category", "all")
    page = int(request.args.get("page", 1))

    if selected_category != "all":
        filtered = [ex for ex in EXHIBITS if ex.category == selected_category]
    else:
        filtered = EXHIBITS

    if query:
        filtered = [ex for ex in filtered if ex.matches_query(query)]

    total_pages = max(1, (len(filtered) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    exhibits_to_show = filtered[start:end]

    answer = ""
    if query:
        if filtered:
            answer = f"تم العثور على {len(filtered)} نتيجة تحتوي على '{query}'."
        else:
            answer = f"لم أجد نتائج لكلمة '{query}'."

    return render_template(
        "index.html",
        exhibits=exhibits_to_show,
        categories=CATEGORIES,
        page=page,
        total_pages=total_pages,
        answer=answer
    )


# ============================================================
#  صفحة المعروض الواحد
# ============================================================
@app.route("/exhibit/<int:ex_id>", methods=["GET", "POST"])
def exhibit_page(ex_id):
    exhibit = next((ex for ex in EXHIBITS if ex.id == ex_id), None)
    if not exhibit:
        return redirect(url_for("index"))

    page = request.args.get("page", 1)
    category = request.args.get("category", "all")
    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            answer = exhibit.bot.answer_question(question)

    return render_template(
        "exhibit.html",
        exhibit=exhibit,
        answer=answer,
        page=page,
        category=category
    )


# ============================================================
#  تشغيل التطبيق
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)