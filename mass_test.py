# =========================================================
# 1. ข้อมูลนำเข้า (Input Data) - ข้อมูลสำหรับทดสอบ
# =========================================================
# ตัวอย่างข้อมูล: Mass Unbalance
f_point_h = [10.0, 46.0, 58.0, 64.0, 77.0, 82.0, 91.0, 116.0]
f_point_v = [10.0, 43.0, 53.0, 69.0, 73.0, 87.0, 94.0, 112.0]
f_point_a = [40.0, 52.0, 67.0, 78.0, 89.0, 93.0, 112.0]

v_h_data = [72.0, 0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1]
v_v_data = [62.0, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1]
v_a_data = [1.5, 1.0, 0.8, 0.5, 0.4, 0.2, 0.1]

rpm = 600 # round per minute

# =========================================================
# 2. การคำนวณและแปลงความถี่เป็น Order (Calculations)
# =========================================================
running_speed_hz = rpm / 60.0  

order_h = [round(val / running_speed_hz, 2) for val in f_point_h]
order_v = [round(val / running_speed_hz, 2) for val in f_point_v]
order_a = [round(val / running_speed_hz, 2) for val in f_point_a]

set_order_h = set(order_h)
set_order_v = set(order_v)
set_order_a = set(order_a)

max_val_h = max(v_h_data)
max_index_h = v_h_data.index(max_val_h)
f_at_max_h = f_point_h[max_index_h]
max_order_h = round(f_at_max_h / running_speed_hz, 2)

max_val_v = max(v_v_data)
max_index_v = v_v_data.index(max_val_v)
f_at_max_v = f_point_v[max_index_v]
max_order_v = round(f_at_max_v / running_speed_hz, 2)

max_val_a = max(v_a_data)
max_index_a = v_a_data.index(max_val_a)
f_at_max_a = f_point_a[max_index_a]
max_order_a = round(f_at_max_a / running_speed_hz, 2)

# =========================================================
# 3. เตรียมตัวแปรเช็คเงื่อนไข (Order Mapping)
# =========================================================
has_1x_h = 1.0 in set_order_h
has_2x_h = 2.0 in set_order_h
has_3x_h = 3.0 in set_order_h

has_1x_v = 1.0 in set_order_v
has_2x_v = 2.0 in set_order_v
has_3x_v = 3.0 in set_order_v

has_1x_a = 1.0 in set_order_a
has_2x_a = 2.0 in set_order_a
has_3x_a = 3.0 in set_order_a

oil_whirl_h = [o for o in set_order_h if 0.40 <= o <= 0.48]
oil_whirl_v = [o for o in set_order_v if 0.40 <= o <= 0.48]
oil_whirl_a = [o for o in set_order_a if 0.40 <= o <= 0.48]

harmonics_h = [o for o in set_order_h if o in [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
harmonics_v = [o for o in set_order_v if o in [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
harmonics_a = [o for o in set_order_a if o in [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]

other_harm_h = [o for o in set_order_h if o in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
other_harm_v = [o for o in set_order_v if o in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
other_harm_a = [o for o in set_order_a if o in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]

fractional_h = [o for o in set_order_h if o % 1 == 0.5]
fractional_v = [o for o in set_order_v if o % 1 == 0.5]
fractional_a = [o for o in set_order_a if o % 1 == 0.5]

# =========================================================
# 4. ลอจิกการวิเคราะห์ปัญหา (Diagnostics Logic)
# =========================================================
finding = ""
causes = []

if (oil_whirl_h and oil_whirl_v) and not oil_whirl_a:
    if not harmonics_h and not harmonics_v:
        finding = "Order ช่วง 0.40X - 0.48X โดดเด่นในแนวรัศมี (H และ V) โดยไม่มีในแนวแกน (A)"
        causes = ["Oil Whirl Instability (ฟิล์มน้ำมันหมุนวน)"]
    else:
        finding = "Order ช่วง 0.40X - 0.48X ในแนวรัศมี แต่พบฮาร์มอนิกปะปนอยู่ด้วย"
        causes = ["อาการ Oil Whirl ซ้อนทับกับปัญหาอื่น เช่น Journal Bearings Wear หรือ Looseness"]

elif fractional_h and fractional_v:
    if max_val_h > max_val_a or max_val_v > max_val_a:
        finding = "ความถี่เศษส่วน (0.5X, 1.5X...) โดดเด่นในแนวรัศมี (H หรือ V)"
        causes = [
            "Journal Bearings Wear (ลูกปืนกาบสึกหรอจนเกิดช่องว่างมากเกินไป)",
            "Mechanical Looseness Type C (การสวมประกอบหลวมภายใน)",
            "Rotor Rub (โรเตอร์เสียดสี)",
            "Mechanical Looseness Type B (กรณีฐานยึดหลวมรุนแรงมากจนเกิดการกระแทก)"
        ]
    else:
        finding = "ความถี่เศษส่วน แต่ความสั่นสะเทือนในแนวแกน (A) กลับสั่นแรงที่สุด"
        causes = ["Rotor Rub บริเวณ Thrust Bearing", "จุดยึดแท่นเครื่องหลวมรุนแรงในแนวแกน"]

elif (has_1x_h and has_2x_h and has_3x_h) and (has_1x_v and has_2x_v and has_3x_v) and \
     not (has_1x_a or has_2x_a or has_3x_a) and not (other_harm_h or other_harm_v) and \
     (max_order_h == 2.0 or max_order_v == 2.0):
    finding = "Order 1X, 2X, 3X ครบชุดทั้ง 2 แกนในแนวรัศมี (H, V) โดย 2X เป็นค่าสูงสุด และไม่มี Order อื่นกวน"
    causes = ["Parallel Misalignment (เยื้องศูนย์แบบขนาน)"]

elif (has_3x_h or other_harm_h or has_3x_v or other_harm_v) and (has_1x_h and has_1x_v):
    if max_val_h > max_val_a or max_val_v > max_val_a:
        finding = "1X ร่วมกับฮาร์มอนิกหางยาว (3X, 4X...) ในแนวรัศมี โดยไม่มีความถี่เศษส่วน"
        causes = [
            "Mechanical Looseness Type B (หลวมที่ฐานยึดโครงสร้าง หรือแท่นร้าว)",
            "Journal Bearings Wear หรือ Looseness Type C (ระยะเริ่มต้น)"
        ]
    else:
        finding = "1X ร่วมกับฮาร์มอนิกหางยาว ในแนวรัศมี แต่ความสั่นในแนวแกน (A) กลับสูงที่สุด"
        causes = ["ปัญหาแท่นเครื่องโก่งตัวอย่างรุนแรง (Soft Foot)"]

elif has_1x_h and has_1x_v:
    if has_1x_a:
        if not harmonics_h and not harmonics_v and not harmonics_a:
            finding = "1X ครบทั้งสามแกน (H, V, A) โดยไม่มีฮาร์มอนิกอื่นปะปน"
            causes = ["Overhung Rotor Unbalance (โรเตอร์ยื่นมีความไม่สมดุล)"]
        else:
            finding = "1X ครบทั้งสามแกน แต่พบความถี่ฮาร์มอนิกแทรกอยู่ด้วย"
            causes = ["Overhung Rotor ร่วมกับปัญหาหลวม (Looseness)"]
    else:
        if has_2x_h or has_2x_v:
            finding = "1X โดดเด่นในแนวรัศมี (H, V) และมียอด 2X ปรากฏขึ้นมาด้วย (แต่ไม่มี 3X, 4X...)"
            causes = ["Mechanical Looseness Type A (ความหลวมของโครงสร้าง/ฐานเครื่อง)"]
        else:
            finding = "1X ล้วนๆ ในแนวรัศมี (H, V) โดยไม่มียอด 2X หรือ Order อื่นปะปนเลย"
            causes = [
                "Mass Unbalance (ไม่สมดุลมวลแบบ Force, Couple, Dynamic)", 
                "Eccentric Rotor (โรเตอร์เยื้องศูนย์)"
            ]

elif has_1x_h or has_1x_v:
    finding = "1X โดดเด่นเพียงแกนเดียวในแนวรัศมี (พบใน H หรือ V เพียงแกนเดียว)"
    causes = ["Directional Resonance (ความถี่สั่นพ้องเฉพาะทิศทาง)"]

elif (has_1x_a or has_2x_a or has_3x_a) and \
     not (has_1x_h or has_2x_h or has_3x_h or has_1x_v or has_2x_v or has_3x_v):
    if not other_harm_a: 
        if has_3x_a:
            finding = "Order 1X, 2X, 3X เกิดขึ้นเฉพาะในแนวแกน (Axial) ล้วนๆ โดยไม่มีแกนรัศมีมาปะปน"
            causes = ["Angular Misalignment (เยื้องศูนย์แบบเชิงมุม)", "Bearing Cocked on Shaft (ลูกปืนเอียงบนเพลา)"]
        elif (max_order_a == 1.0 or max_order_a == 2.0):
            finding = "1X และ/หรือ 2X โดดเด่นเป็นค่าสูงสุดในแนวแกน (Axial) โดยไม่มี Order อื่นรบกวน"
            causes = ["Angular Misalignment (เยื้องศูนย์แบบเชิงมุม)", "Bent Shaft (เพลาคด/งอ)"]
    else:
        finding = "1X, 2X, 3X ในแนวแกน (Axial) แต่มีฮาร์มอนิกที่สูงกว่าปะปนอยู่ด้วย"
        causes = ["Severe Misalignment (เยื้องศูนย์รุนแรง)", "แท่นประกอบไม่ได้ระดับอย่างมาก"]

else:
    finding = "ไม่พบแพทเทิร์น Order ที่ตรงกับปัญหาพื้นฐานทางกล (Low-frequency faults)"
    causes = [
        "ตรวจสอบปัญหาหมวดความถี่สูง (เช่น ลูกปืนแตก, Gear mesh)", 
        "ตรวจสอบความถี่ Sub-synchronous อื่นๆ (เช่น สายพาน)"
    ]

# =========================================================
# 5. แสดงผลหน้าจอ (Clean UI Output)
# =========================================================
print("\n" + "═"*70)
print(" 📊 สรุปค่าสูงสุด (MAX AMPLITUDE)")
print("-" * 70)
print(f"  [H] HORIZONTAL : {max_val_h:>6.1f} mm/s  |  ที่ {f_at_max_h:>5.1f} Hz (Order {max_order_h})")
print(f"  [V] VERTICAL   : {max_val_v:>6.1f} mm/s  |  ที่ {f_at_max_v:>5.1f} Hz (Order {max_order_v})")
print(f"  [A] AXIAL      : {max_val_a:>6.1f} mm/s  |  ที่ {f_at_max_a:>5.1f} Hz (Order {max_order_a})")
print("═"*70)

print("\n" + "⚙️ รายการความถี่ (ORDER) ที่พบ".center(65))
print(f"(อ้างอิง 1X = {running_speed_hz:.1f} Hz)".center(68))
print("-" * 70)
print(f"  [H] แกน H : {sorted(list(set_order_h))}")
print(f"  [V] แกน V : {sorted(list(set_order_v))}")
print(f"  [A] แกน A : {sorted(list(set_order_a))}")
print("═"*70)

print("\n" + " 🎯 ผลการวินิจฉัย (DIAGNOSTIC RESULT) ".center(65, "▒"))
print("\n 🔍 สิ่งที่ตรวจพบ:")
print(f"    - {finding}\n")
print(" ⚠️ ข้อสันนิษฐาน (Possible Causes):")
for i, cause in enumerate(causes, 1):
    print(f"    {i}. {cause}")
print("\n" + "▒"*70 + "\n")