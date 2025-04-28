# il-bank-validator

✅ Israeli Bank Account Validator  
עדכני לפי מסמך מס"ב הרשמי ל־1/12/2024.

---

## ✨ מבוא
חבילה זו מאמתת תקינות של מספרי חשבונות בנק ישראליים לפי כללי מס"ב החדשים.  
היא לא בודקת האם החשבון פעיל — אלא רק אם המספר **חוקי** לפי כללי הבנקים.

> המסמך הרשמי: [מס"ב - בדיקת חוקיות חשבון](https://www.masav.co.il/media/2565/bdikat_hukiot_heshbon.pdf)

---

## 🏦 תמיכה בבנקים

| בנק                  | קוד בנק | תמיכה |
|-----------------------|---------|-------|
| לאומי                 | 10, 34  | ✅ |
| הפועלים               | 12      | ✅ |
| יהב                   | 4       | ✅ |
| דיסקונט / מרכנתיל    | 11, 17  | ✅ |
| מזרחי טפחות           | 20      | ✅ |
| הבינלאומי / פאג"י    | 31, 52  | ✅ |
| בנק הדואר             | 9       | ✅ |
| אוצר החייל            | 14      | ✅ |
| מסד                   | 46      | ✅ |
| סיטי בנק              | 22      | ✅ |
| HSBC                  | 23      | ✅ (חלקי) |
| וואן זירו             | 18      | ✅ |
| בנק אש                | 3       | ✅ |
| גלובל רמיט            | 47      | ✅ |
| GROW                  | 35      | ✅ |
| אופק                  | 15      | ✅ |
| נעמה (שפע ישראל)      | 21      | ✅ |
| ריווייר               | 58      | ✅ |
| ירושלים               | 54      | ❌ אין כללים |
| SBI (State Bank India) | 39     | ❌ אין כללים |

---

## 🚀 התקנה

```bash
pip install il-bank-validator
```

(אם מקומית:)

```bash
git clone https://github.com/EliShteinman/il-bank-validator.git
cd il-bank-validator
pip install .
```

---

## 🧩 דוגמת שימוש

```python
from il_bank_validator import validate_israeli_bank_account

if validate_israeli_bank_account(10, 936, "07869660"):
    print("Valid account!")
else:
    print("Invalid account!")
```

---

## 📄 רישיון

MIT License.
