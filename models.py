from dataclasses import dataclass
from flask import session
import random


# ============================================================
#  نموذج Exhibit
# ============================================================

class Exhibit:
    def __init__(self, _id, name, category, image, period, origin, description):
        # الخصائص الخاصة (Encapsulation)
        self._id = _id
        self._name = name
        self._category = category
        self._image = image
        self._period = period
        self._origin = origin
        self._description = description

    # ======================================================
    # Getters / Setters — التغليف الآمن
    # ========================================================

    # ID — للقراءة فقط ( لانه ثابت setter بدون )
    @property
    def id(self):
        return self._id

    # NAME
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value.strip()) < 2:
            raise ValueError(" اسم المعروض يجب أن يحتوي على حرفين على الأقل.")
        self._name = value.strip()

    # CATEGORY
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value:
            raise ValueError(" لا يمكن ترك فئة المعروض فارغة.")
        self._category = value.strip()

    # IMAGE
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if not value.endswith((".jpg", ".png", ".jpeg", ".webp")):
            raise ValueError(" يجب أن تكون صورة المعروض بصيغة صحيحة مثل JPG أو PNG.")
        self._image = value

    # PERIOD
    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if len(value.strip()) < 3:
            raise ValueError(" اسم الفترة قصير جدًا.")
        self._period = value.strip()

    # ORIGIN
    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        if not value:
            raise ValueError(" يجب تحديد أصل المعروض.")
        self._origin = value.strip()

    # DESCRIPTION
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if len(value.strip()) < 10:
            raise ValueError(" الوصف يجب أن يحتوي على 10 أحرف على الأقل.")
        self._description = value.strip()

    # ========================================================
    #  أساليب إضافية (Methods)
    # ========================================================
    def short_info(self):
        """ملخص بسيط للعرض في الصفحة الرئيسية"""
        return f"{self._name} — {self._period}, {self._origin}"

    def matches_query(self, query: str) -> bool:
        """البحث بالنص"""
        q = query.lower()
        return q in self._name.lower() or q in self._description.lower()

    def str(self):
        """تمثيل نصي للكائن (للطباعة أو التصحيح)"""
        return f"Exhibit({self._id}: {self._name}, {self._category})"
# ============================================================
#  ExhibitBot
# ============================================================
class ExhibitBot:
    def __init__(self, exhibit):
        self.exhibit = exhibit

    def answer_question(self, question: str) -> str:
        q = question.lower()

        greetings = [
            "سؤال رائع! ",
            "يا له من فضول جميل! ",
            "أحب هذا النوع من الأسئلة ",
            "سعيد أنك مهتم بهذا المعروض "
        ]

        intro = self.get_unique_response(greetings, self.exhibit.id)

        if "من أين" in q or "أصل" in q:
            return f"{intro} أصل هذا المعروض من {self.exhibit.origin}."
        elif "متى" in q or "تاريخ" in q or "عمر" in q:
            return f"{intro} يعود تاريخ هذا المعروض إلى {self.exhibit.period}."
        elif "ما هو" in q or "ماذا" in q:
            return f"{intro} هذا {self.exhibit.name}، وهو من {self.exhibit.category}. {self.exhibit.description}"
        elif "كيف" in q:
            return f"{intro} لم يتم توثيق طريقة صنع هذا المعروض بدقة، لكن من المرجح أنه استخدم تقنيات متقدمة في {self.exhibit.period}."
        elif "لماذا" in q:
            return f"{intro} يُعتقد أن سبب صنع {self.exhibit.name} كان لأغراض دينية أو فنية حسب ما توصل إليه المؤرخون."
        elif self.exhibit.name.lower() in q:
            return f"{intro} {self.exhibit.name} من أجمل القطع التي تمثل {self.exhibit.category}."
        else:
            return f"{intro} بصراحة لا أملك إجابة دقيقة عن ذلك، لكن يمكنك قراءة الوصف لمعرفة المزيد."

    def get_unique_response(self, responses, ex_id):
        key = f"seen_responses_{ex_id}"
        seen = session.get(key, [])
        available = [r for r in responses if r not in seen]

        if not available:
            seen = []
            available = responses.copy()

        chosen = random.choice(available)
        seen.append(chosen)
        session[key] = seen
        session.modified = True
        return chosen