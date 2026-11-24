# ---------- 1. ข้อมูลนำเข้า (แก้ตรงนี้) ----------
f_h = [10.0, 4.2, 38.0, 42.0, 58.0, 64.0, 77.0, 82.0, 91.0, 116.0]  # ความถี่ (Hz)
f_v = [10.0, 26.0, 4.3, 48.0, 53.0, 69.0, 73.0, 87.0, 94.0, 112.0]
f_a = [12.0, 21.0, 32.0, 49.0, 52.0, 67.0, 78.0, 89.0, 93.0, 112.0]

v_h = [78.0, 83.0, 2.0, 0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1]  # แอมพลิจูด (mm/s)
v_v = [83.0, 2.0, 73.0, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1]
v_a = [3.0, 2.0, 1.0, 1.5, 1.0, 0.8, 0.5, 0.4, 0.2, 0.1]

rpm = 600  # รอบต่อนาที

# ---------- 2. ค่าตั้ง (ปรับตามเครื่องจริงได้) ----------
TOL = 0.08                 # Order คลาดได้ +/- เท่านี้
REL_TOL = 0.01             # เผื่อเพิ่มตามลำดับฮาร์มอนิก (n x 1%)
HARM_MAX = 10              # นับฮาร์มอนิกถึง 10X
MIN_PERCENT = 0.10         # ตัดนอยส์: ยอดต้องสูง >= 10% ของยอดสูงสุด
MIN_ABS = 1.0              # และ >= ค่านี้ (mm/s)
REF_GLOBAL = True          # True = เทียบกับยอดสูงสุดของทุกแกน
ONE_X_RATIO = 2.0          # 1X ต้องสูงกว่ายอดอื่นกี่เท่า ถึงเรียกว่า "เด่นชัด"
AXIAL_RATIO = 0.5          # แกน A สูงกี่ส่วนของแนวรัศมี ถึงเรียกว่า "สูง"
MANY = 4                   # ฮาร์มอนิกต่อเนื่องกี่ตัวขึ้นไปถึงเรียกว่า "หลายตัว"
RUB_MAX_ORDER = 5          # Rotor Rub นับเศษส่วนไม่เกินกี่ X
RUB_MIN_POSITIONS = 2      # Rotor Rub ต้องเจอเศษส่วนกี่ตำแหน่ง
CTYPE_MIN_POSITIONS = 2    # Looseness C ต้องเจอเศษส่วนกี่ตำแหน่ง
CTYPE_MIN_HARMONICS = 3    # Looseness C ต้องมีฮาร์มอนิกกี่ตัว
REQUIRE_BOTH_AXES = True   # อาการแนวรัศมี: True = ต้องเจอทั้ง H และ V
OIL_WHIRL_ONE_AXIS = True  # Oil Whirl: True = เจอแกนเดียวก็พอ (ไม่ผูกกับค่าด้านบน)
SHOW_UNEXPLAINED = True    # เตือนยอดสูงสุดที่ไม่ตรง Order ที่รู้จัก
ZONE_LIMITS = (1.4, 2.8, 4.5)  # ระดับความรุนแรง ISO 20816-3 กลุ่ม 2 (ตัวอย่าง, ค่า RMS)


# ---------- 3. ฟังก์ชันช่วย ----------
def is_num(x):
    return (isinstance(x, (int, float)) and not isinstance(x, bool)
            and x == x and abs(x) != float("inf"))


def make_orders(freqs, amps, run_hz, ref=None):
    if len(freqs) != len(amps):
        raise ValueError("จำนวนความถี่กับแอมพลิจูดไม่เท่ากัน")
    if not freqs:
        raise ValueError("ไม่มีข้อมูลในแกนนี้ (ลิสต์ว่าง)")
    if any(not is_num(f) or f <= 0 for f in freqs):
        raise ValueError("ความถี่ต้องเป็นตัวเลขบวก")
    if any(not is_num(a) or a < 0 for a in amps):
        raise ValueError("แอมพลิจูดต้องเป็นตัวเลขไม่ติดลบ")
    limit = max(MIN_ABS, MIN_PERCENT * (ref if ref is not None else max(amps)))
    orders = {}
    for f, a in zip(freqs, amps):
        if a >= limit:
            o = round(f / run_hz, 6)
            orders[o] = max(a, orders.get(o, 0.0))  
    return orders


def near(o, n):
    return abs(o - n) <= TOL + REL_TOL * n


def amp_at(orders, n):
    return max([a for o, a in orders.items() if near(o, n)], default=0.0)


def is_whirl(o):
    return 0.42 <= o <= 0.48  


def is_fraction(o):
    if is_whirl(o):
        return False
    half = abs(o % 1.0 - 0.5) <= 0.03
    sub = o < 0.9 and any(abs(o - 1.0 / n) <= 0.03 for n in (3, 4, 5, 6))
    return half or sub


def is_explained(o):
    n = round(o * 2) / 2
    return near(o, n) or is_fraction(o) or is_whirl(o)


def has_run(values, length):
    run, prev = 0, None
    for v in values:
        run = run + 1 if prev is not None and v == prev + 1 else 1
        if run >= length:
            return True
        prev = v
    return False


def look(orders):
    x1 = amp_at(orders, 1)
    others = [a for o, a in orders.items() if not near(o, 1)]
    r = {
        "x1": x1,
        "x2": amp_at(orders, 2),
        "x3": amp_at(orders, 3),
        "harmonics": [n for n in range(2, HARM_MAX + 1) if amp_at(orders, n) > 0],
        "fractions": [o for o in orders if is_fraction(o)],
        "whirl": [o for o in orders if is_whirl(o)],
        "top": max(orders, key=orders.get) if orders else None,
        "biggest": max([amp_at(orders, n) for n in range(1, HARM_MAX + 1)]),
        "one_x_clear": x1 > 0 and (not others or x1 >= ONE_X_RATIO * max(others)),
        "one_x_top": x1 > 0 and x1 >= max(orders.values(), default=0),
    }
    r["fractions_low"] = [o for o in r["fractions"] if o <= RUB_MAX_ORDER]
    return r


def severity(level):
    names = ["Zone A (ดี)", "Zone B (ยอมรับได้)", "Zone C (เริ่มเกินเกณฑ์)", "Zone D (อันตราย)"]
    return next((n for n, lim in zip(names, ZONE_LIMITS) if level <= lim), names[-1])


def level_of(amps):
    return sum(x * x for x in amps) ** 0.5


def fmt(orders):
    return [round(o, 2) for o in sorted(orders)]


# ---------- 4. ตัววินิจฉัย ----------
def diagnose(H, V, A):
    h, v, a = look(H), look(V), look(A)
    radial = [("H", h), ("V", v)]
    radial_wins = max(h["biggest"], v["biggest"]) >= a["biggest"]
    axial_high = a["biggest"] > 0 and a["biggest"] >= AXIAL_RATIO * max(h["biggest"], v["biggest"])
    out = []
    def ok(names):  # อาการแนวรัศมี: ต้องเจอทั้งสองแกน (หรือแกนเดียวถ้าปิดกฎ)
        return len(names) == 2 or (len(names) == 1 and not REQUIRE_BOTH_AXES)
    def add(title, *notes):
        out.append((title, list(notes)))
    # 1) Mass Unbalance / Looseness Type A (1X ล้วน)
    unbalance = ok([n for n, f in radial if f["one_x_clear"]]) and radial_wins
    if unbalance:
        if a["x1"] > 0 and a["x1"] >= 0.3 * max(h["x1"], v["x1"]):
            add("Overhung Rotor Unbalance (หรือ Couple Unbalance)", "1X เด่นทั้งแนวรัศมีและแนวแกน")
        else:
            add("Mass Unbalance (Force หรือ Couple)",
                "1X สูงกว่ายอดอื่นอย่างน้อย %g เท่า ในแนวรัศมี" % ONE_X_RATIO)
        add("Mechanical Looseness Type A (ฐานเครื่อง/แท่นยึดอ่อนแอ, Soft Foot)",
            "สเปกตรัม 1X ล้วน เหมือนกับ Unbalance", "ควรตรวจโบลต์/ฐานราก")
    # 1b) 1X เป็นยอดสูงสุด แต่มียอดอื่นสูงปน
    if not unbalance and radial_wins:
        names = [n for n, f in radial if f["one_x_top"] and not f["fractions"]
                 and not f["whirl"] and len(f["harmonics"]) < MANY]
        if ok(names):
            big = set()
            for orders in (H, V):
                if orders:
                    top_amp = max(orders.values())
                    big |= {round(o, 2) for o, x in orders.items()
                            if not near(o, 1) and x >= 0.5 * top_amp}
            add("Mass Unbalance (เป็นไปได้ แต่ 1X ไม่ได้เด่นชัด)",
                "1X เป็นยอดสูงสุดในแนวรัศมี แต่มียอดอื่นสูงปนอยู่ที่ Order " + str(sorted(big)),
                "ไม่ใช่สเปกตรัม 1X ล้วนตามตาราง ควรหาสาเหตุของยอดอื่นด้วย")
    # 2) แนวแกนสูง: Angular, Bent Shaft, Cocked Bearing
    top = a["top"]
    if axial_high and not unbalance and top is not None and any(near(top, n) for n in (1, 2, 3)):
        severe_note = ["มี 4X ขึ้นไปปนด้วย แสดงว่าค่อนข้างรุนแรง"] if any(k >= 4 for k in a["harmonics"]) else []
        add("Angular Misalignment (เยื้องศูนย์เชิงมุม)", "แนวแกนสูง มี 1X/2X/3X", *severe_note)
        if near(top, 1) or near(top, 2):
            add("Bent Shaft (เพลาคด/งอ)", "แนวแกนสูง โดย 1X เด่น (หรือ 2X ถ้าคดใกล้คัปปลิง)")
        if a["x3"] > 0 and (a["x1"] > 0 or a["x2"] > 0):
            add("Bearing Cocked on Shaft (ลูกปืนเอียงบนเพลา)", "แนวแกนสูง มี 1X, 2X, 3X")
    # 3) Parallel Misalignment: 1X, 2X + 3X หรือ 4X-8X (ไม่มีเศษส่วน)
    par = [n for n, f in radial if f["x1"] > 0 and f["x2"] > 0 and not f["fractions"]
           and (f["x3"] > 0 or any(4 <= k <= 8 for k in f["harmonics"]))]
    severe = any(4 <= k <= 8 for n, f in radial if n in par for k in f["harmonics"])
    if ok(par) and radial_wins:
        note = ["มียอด 4X-8X แสดงว่ารุนแรง และสเปกตรัมจะคล้าย Looseness"] if severe else []
        add("Parallel Misalignment (เยื้องศูนย์แบบขนาน)",
            "แนวรัศมี (" + "/".join(par) + ") มี 1X, 2X ร่วมกับ 3X หรือฮาร์มอนิกสูงกว่า", *note)
    # 4) Looseness Type B: 1X + 2X/3X ไม่มีเศษส่วน
    lb = [n for n, f in radial if f["x1"] > 0 and (f["x2"] > 0 or f["x3"] > 0)
          and not f["fractions"] and len(f["harmonics"]) < MANY]
    if ok(lb) and radial_wins:
        add("Mechanical Looseness Type B (โครงสร้าง/ฐานร้าว หรือโบลต์ขาตั้งแบริ่งหลวม)",
            "แนวรัศมี (" + "/".join(lb) + ") มี 1X ร่วมกับ 2X/3X ไม่มีความถี่เศษส่วน",
            "สเปกตรัมคล้าย Parallel Misalignment")
    # 5) Looseness Type C: เศษส่วนหลายตำแหน่ง + ฮาร์มอนิกหลายตัว
    lc = [n for n, f in radial if len(f["fractions_low"]) >= CTYPE_MIN_POSITIONS
          and len(f["harmonics"]) >= CTYPE_MIN_HARMONICS]
    if ok(lc):
        fr = fmt({o for n, f in radial if n in lc for o in f["fractions_low"]})
        add("Mechanical Looseness Type C (ประกอบหลวมภายใน เช่น ลูกปืนกับเสื้อ, ปลอกแบริ่งสึก)",
            "พบความถี่เศษส่วน " + str(fr) + " ร่วมกับฮาร์มอนิกหลายตัว",
            "ตรวจคลื่นเวลา: Type C จะเห็นคลื่นถูกตัดทอน")
    # 6) Rotor Rub: เศษส่วนหลายตำแหน่ง
    rub = [n for n, f in radial if len(f["fractions_low"]) >= RUB_MIN_POSITIONS]
    if ok(rub):
        cnt = max(len(f["fractions_low"]) for n, f in radial if n in rub)
        add("Rotor Rub (โรเตอร์เสียดสี) ความเป็นไปได้: " + ("สูง" if cnt >= 3 else "เป็นไปได้"),
            "พบความถี่เศษส่วน/ซับฮาร์มอนิก " + str(cnt) + " ตำแหน่ง",
            "ตรวจคลื่นเวลาว่าถูกตัดแบนหรือไม่")
    # 7) Sleeve Bearing: ฮาร์มอนิกเรียงต่อเนื่องกันอย่างน้อย MANY ตัว
    wear = [n for n, f in radial if has_run(f["harmonics"], MANY)]
    if ok(wear):
        detail = "  ".join("%s: %s" % (n, " ".join("%dX" % k for k in f["harmonics"]))
                           for n, f in radial if n in wear)
        add("Sleeve Bearing Wear / Excessive Clearance", "ฮาร์มอนิกเรียงต่อเนื่องในแนวรัศมี -> " + detail)
    # 8) Oil Whirl: 0.42-0.48X
    wh = [n for n, f in radial if f["whirl"]]
    if ok(wh) or (wh and OIL_WHIRL_ONE_AXIS):
        od = fmt({o for n, f in radial if n in wh for o in f["whirl"]})
        add("Oil Whirl Instability (ฟิล์มน้ำมันไม่เสถียร)",
            "พบยอด " + str(od) + "X ในแนวรัศมี (" + "/".join(wh) + ")",
            "ถ้าเพิ่มรอบแล้วความถี่ยอดนี้ไม่ขยับตาม ให้พิจารณา Oil Whip")
    return out


def explain(H, V, A):
    h, v, a = look(H), look(V), look(A)
    lines = ["แกน %s ไม่มียอดที่ผ่านเกณฑ์" % n for n, o in (("H", H), ("V", V), ("A", A)) if not o]
    for n, f, o in (("H", h, H), ("V", v, V)):
        if o and not (f["x1"] or f["x2"] or f["x3"]):
            top3 = sorted(o, key=o.get, reverse=True)[:3]
            lines.append("แกน %s ไม่มี 1X/2X/3X เลย ยอดแรงสุดอยู่ที่ Order %s"
                         % (n, ", ".join("%.2f" % x for x in top3)))
    checks = [
        ("1X", lambda f: f["x1"] > 0),
        ("2X", lambda f: f["x2"] > 0),
        ("3X", lambda f: f["x3"] > 0),
        ("ความถี่เศษส่วน (0.5X, 1.5X ฯลฯ)", lambda f: len(f["fractions_low"]) > 0),
        ("Oil Whirl (0.42-0.48X)", lambda f: len(f["whirl"]) > 0),
        ("ฮาร์มอนิก 4X ขึ้นไป", lambda f: any(k >= 4 for k in f["harmonics"])),
    ]
    for label, has in checks:
        found = [n for n, f in (("H", h), ("V", v)) if has(f)]
        if len(found) == 1:
            lines.append("%s พบในแกน %s เท่านั้น" % (label, found[0]))
    for n, f in (("H", h), ("V", v)):
        if f["x1"] > 0 and not f["one_x_clear"]:
            lines.append("1X ในแกน %s ไม่เด่นพอ (มียอดอื่นสูงเกือบเท่า)" % n)
    if A:
        if a["biggest"] == 0:
            lines.append("แกน A ไม่มียอดจำนวนเต็มที่ผ่านเกณฑ์")
        elif a["biggest"] >= AXIAL_RATIO * max(h["biggest"], v["biggest"]):
            lines.append("แกน A สูง แต่ยอดสูงสุดไม่ได้อยู่ที่ 1X/2X/3X")
        else:
            lines.append("แกน A ต่ำกว่า %d%% ของแนวรัศมี จึงไม่ถือเป็นแนวแกนสูง" % (AXIAL_RATIO * 100))
    return lines


def axis_summary(name, orders):
    if not orders:
        return " %s: ไม่มียอดที่ผ่านเกณฑ์" % name
    f = look(orders)
    cell = lambda x: "%.1f" % x if x > 0 else "-"
    frac = str(len(f["fractions_low"])) if f["fractions_low"] else "-"
    top = max(orders, key=orders.get)
    return " %s: 1X=%s  2X=%s  3X=%s  เศษส่วน=%s  ยอดสูงสุด %.2fX (%.1f)" % (
        name, cell(f["x1"]), cell(f["x2"]), cell(f["x3"]), frac, top, orders[top])

# ---------- 5. รันและแสดงผล ----------
def main():
    if not is_num(rpm) or rpm <= 0:
        raise ValueError("rpm ต้องเป็นตัวเลขมากกว่า 0")
    for name, f, a in (("H", f_h, v_h), ("V", f_v, v_v), ("A", f_a, v_a)):
        try:
            make_orders(f, a, 1.0)
        except ValueError as e:
            raise ValueError("แกน %s: %s" % (name, e))
    run = rpm / 60.0
    ref = max(max(v_h), max(v_v), max(v_a)) if REF_GLOBAL else None
    H = make_orders(f_h, v_h, run, ref)
    V = make_orders(f_v, v_v, run, ref)
    A = make_orders(f_a, v_a, run, ref)
    print("\n" + "=" * 50)
    print(" 📊 Order ที่ผ่านเกณฑ์ (1X = %s Hz)" % run)
    print("=" * 50)
    print(" 🟢 แกน H : %s" % fmt(H))
    print(" 🔵 แกน V : %s" % fmt(V))
    print(" 🟣 แกน A : %s" % fmt(A))
    for name, orders, amps in (("H", H, v_h), ("V", V, v_v), ("A", A, v_a)):
        if not orders:
            thr = max(MIN_ABS, MIN_PERCENT * (ref if ref is not None else max(amps)))
            print(" ⚠️ แกน %s ไม่มียอดที่ผ่านเกณฑ์ (ต้องไม่ต่ำกว่า %.1f mm/s) จึงไม่นำมาวิเคราะห์" % (name, thr))
    print("\n 🧾 สรุปแต่ละแกน")
    print(" รอบเครื่อง %s rpm (1X = %s Hz)" % (rpm, run))
    for name, orders in (("H", H), ("V", V), ("A", A)):
        print(axis_summary(name, orders))
    print("\n" + "=" * 50)
    print(" 🎯 ผลการวินิจฉัย")
    print("=" * 50)
    results = diagnose(H, V, A)
    if not results:
        print(" ❌ ไม่พบแพทเทิร์นที่ตรงกับ 6 หัวข้อที่ครอบคลุม")
        print(" เหตุผล:")
        for line in explain(H, V, A):
            print("    - " + line)
        print(" ไม่พบแพทเทิร์นไม่ได้แปลว่าอุปกรณ์ปกติ ควรตรวจสาเหตุอื่นเพิ่ม")
    else:
        if len(results) > 1:
            print(" ℹ️ พบที่เข้าได้ %d แบบ (สเปกตรัมซ้อนกัน ต้องแยกด้วยข้อมูลหน้างาน)\n" % len(results))
        for i, (title, notes) in enumerate(results, 1):
            print(" %d. ⚠️ %s" % (i, title))
            for note in notes:
                print("      - " + note)
    if SHOW_UNEXPLAINED:
        for name, orders in (("H", H), ("V", V), ("A", A)):
            if orders:
                top = max(orders, key=orders.get)
                if not is_explained(top):
                    print(" ⚠️ แกน %s: ยอดสูงสุดอยู่ที่ Order %.2f (%.1f mm/s) ไม่ตรงกับแพทเทิร์นที่รู้จัก"
                          % (name, top, orders[top]))
                    print("      ควรตรวจสาเหตุอื่น เช่น Resonance, ลูกปืน, เกียร์, สายพาน, ใบพัด\n")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()