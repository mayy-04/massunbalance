# ข้อมูลความถี่ (Hz) 
f_point_h = [10.0, 20.0, 37.0, 42.0, 58.0, 64.0, 77.0, 82.0, 91.0, 116.0]
f_point_v = [10.0, 22.0, 37.0, 48.0, 53.0, 69.0, 73.0, 87.0, 94.0, 112.0]
f_point_a = [18.0, 23.0, 37.0, 49.0, 52.0, 67.0, 78.0, 89.0, 93.0, 112.0]

# ข้อมูลความเร็ว (mm/s) 
v_h_data = [72.0, 91.5, 61.0, 0.8, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1] 
v_v_data = [72.0, 62.0, 75.0, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1] 
v_a_data = [38.0, 42.0, 50.0, 1.5, 1.0, 0.8, 0.5, 0.4, 0.2, 0.1]

rpm = 600 # round per minute

running_speed_hz = rpm / 60.0  # 600 / 60 = 10.0 Hz (1X หรือ Order 1)

# แปลงความถี่ทุกตัวให้เป็น Order (ปัดเศษ 2 ตำแหน่ง) และตัดค่าซ้ำด้วย set() เพื่อใช้เช็คเงื่อนไข
order_h = [round(val / running_speed_hz, 2) for val in f_point_h]
order_v = [round(val / running_speed_hz, 2) for val in f_point_v]
order_a = [round(val / running_speed_hz, 2) for val in f_point_a]

set_order_h = set(order_h)
set_order_v = set(order_v)
set_order_a = set(order_a)

# --- หาค่าสูงสุด (Max) และ Order ที่สั่นแรงที่สุดในแต่ละแกน ---
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

print("\n" + "="*50)
print(" 📊 สรุปค่าสูงสุด (MAX AMPLITUDE)")
print("="*50)
print(f" 🟢 HORIZONTAL : {max_val_h:>5.1f} mm/s  (ที่ {f_at_max_h:>5.1f} Hz / Order {max_order_h})")
print(f" 🔵 VERTICAL   : {max_val_v:>5.1f} mm/s  (ที่ {f_at_max_v:>5.1f} Hz / Order {max_order_v})")
print(f" 🟣 AXIAL      : {max_val_a:>5.1f} mm/s  (ที่ {f_at_max_a:>5.1f} Hz / Order {max_order_a})")

print("\n" + "-"*50)
print(f" ⚙️ รายการ Order ที่พบ (1X = {running_speed_hz} Hz)")
print("-"*50)
print(f" 🟢 แกน H : {sorted(list(set_order_h))}")
print(f" 🔵 แกน V : {sorted(list(set_order_v))}")
print(f" 🟣 แกน A : {sorted(list(set_order_a))}")

print("\n" + "="*50)
print(" 🎯 ผลการวินิจฉัย (DIAGNOSTIC RESULT)")
print("="*50)

# --- เตรียมตัวแปรเช็คเงื่อนไขแยกตามแกน H, V และ A ---
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

# ดักจับเฉพาะฮาร์มอนิก 4X ขึ้นไป (ใช้เช็คความบริสุทธิ์ของคลื่น Misalignment)
other_harm_h = [o for o in set_order_h if o in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
other_harm_v = [o for o in set_order_v if o in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
other_harm_a = [o for o in set_order_a if o in [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]

fractional_h = [o for o in set_order_h if o % 1 == 0.5]
fractional_v = [o for o in set_order_v if o % 1 == 0.5]
fractional_a = [o for o in set_order_a if o % 1 == 0.5]

# 1. หมวด Oil Whirl
if (oil_whirl_h and oil_whirl_v) and not oil_whirl_a:
    if not harmonics_h and not harmonics_v:
        print(" 💡 ตรวจพบ: Order ช่วง 0.40X - 0.48X โดดเด่นในแนวรัศมี (H และ V) โดยไม่มีในแนวแกน (A)")
        print(" ⚠️ ข้อสันนิษฐาน: Oil Whirl Instability ")
    else:
        print(" 💡 ตรวจพบ: Order ช่วง 0.40X - 0.48X ในแนวรัศมี แต่พบฮาร์มอนิก (2X, 3X, 4X...) ปะปนอยู่ด้วย")
        print(" ⚠️ ข้อสันนิษฐาน: มีอาการ Oil Whirl ซ้อนทับกับปัญหาอื่น เช่น Journal Bearings Wear หรือ Looseness")

# 2. หมวดความถี่เศษส่วน (Fractional Harmonics: 0.5X, 1.5X...) + ฮาร์มอนิกเต็มหน่วย
elif fractional_h and fractional_v:
    if max_val_h > max_val_a or max_val_v > max_val_a:
        print(" 💡 ตรวจพบ: ความถี่เศษส่วน (0.5X, 1.5X...) โดดเด่นในแนวรัศมี (H หรือ V)")
        print(" ⚠️ ข้อสันนิษฐาน: ปัญหาจาก 'ช่องว่าง' หรือ 'การกระแทก/เสียดสี' เป็นไปได้ดังนี้:")
        print("    - Journal Bearings Wear ")
        print("    - Mechanical Looseness Type C ")
        print("    - Rotor Rub ")
        print("    - Mechanical Looseness Type B ")
    else:
        print(" 💡 ตรวจพบ: ความถี่เศษส่วน แต่ความสั่นสะเทือนในแนวแกน (A) กลับสั่นแรงที่สุด")
        print(" ⚠️ ข้อสันนิษฐาน: อาจเป็น Rotor Rub บริเวณ Thrust Bearing หรือจุดยึดแท่นเครื่องหลวมรุนแรงในแนวแกน")

# 3. หมวด Parallel Misalignment (เยื้องศูนย์แบบขนาน)
# บังคับเข้มงวด: ต้องเจอ 1X, 2X, 3X ครบทั้ง 3 ออเดอร์ ใน "ทั้งแกน H และ V" พร้อมกัน
elif (has_1x_h and has_2x_h and has_3x_h) and (has_1x_v and has_2x_v and has_3x_v) and \
     not (has_1x_a or has_2x_a or has_3x_a) and \
     not (other_harm_h or other_harm_v) and \
     (max_order_h == 2.0 or max_order_v == 2.0):
    print(" 💡 ตรวจพบ: Order 1X, 2X, 3X ครบชุดทั้ง 2 แกนในแนวรัศมี (H และ V) โดย 2X เป็นค่าสูงสุด และไม่เกิดในแกนอื่นหรือ Order อื่นรบกวน")
    print(" ⚠️ ข้อสันนิษฐาน: Parallel Misalignment ")

# 4. หมวด Looseness Type B / Bearing Wear 
# บังคับว่า Type B ต้องมีคลื่น "หางยาว" คือต้องเจอ 3X หรือ 4X ขึ้นไปเท่านั้น (ถ้ามีแค่ 2X จะไม่เข้าหมวดนี้)
elif (has_3x_h or other_harm_h or has_3x_v or other_harm_v) and (has_1x_h and has_1x_v):
    if max_val_h > max_val_a or max_val_v > max_val_a:
        print(" 💡 ตรวจพบ: 1X ร่วมกับฮาร์มอนิกหางยาว (3X, 4X...) ในแนวรัศมี โดยไม่มีความถี่เศษส่วน")
        print(" ⚠️ ข้อสันนิษฐาน: อาการหลวมระยะเริ่มต้น (ยังไม่มีการกระแทกรุนแรงจนเกิด 0.5X)")
        print(" ⚠️ ข้อสันนิษฐาน: เป็นไปได้ทั้ง:")
        print("    - Mechanical Looseness Type B ")
        print("    - Journal Bearings Wear หรือ Looseness Type C ")
    else:
        print(" 💡 ตรวจพบ: 1X ร่วมกับฮาร์มอนิกหางยาว ในแนวรัศมี แต่ความสั่นสะเทือนในแนวแกน (A) กลับสูงที่สุด")
        print(" ⚠️ ข้อสันนิษฐาน: อาจเป็นปัญหาแท่นเครื่องโก่งตัวอย่างรุนแรง ")

# 5. หมวด Unbalance (Mass และ Overhung) และ Looseness Type A
elif has_1x_h and has_1x_v:
    if has_1x_a:
        if not harmonics_h and not harmonics_v and not harmonics_a:
            print(" 💡 ตรวจพบ: 1X ครบทั้งสามแกน (H, V, A) โดยไม่มีฮาร์มอนิกอื่นปะปน")
            print(" ⚠️ ข้อสันนิษฐาน: Overhung Rotor Unbalance ")
        else:
            print(" 💡 ตรวจพบ: 1X ครบทั้งสามแกน แต่พบความถี่ฮาร์มอนิกแทรกอยู่ด้วย")
            print(" ⚠️ ข้อสันนิษฐาน: อาจเป็น Overhung Rotor ร่วมกับปัญหาหลวม (Looseness)")
    else:
        # --- แยก Mass Unbalance กับ Looseness Type A ด้วยยอด 2X ---
        if has_2x_h and has_2x_v:
            print(" 💡 ตรวจพบ: 1X โดดเด่นในแนวรัศมี (H, V) และมียอด 2X ปรากฏขึ้นมาด้วย (แต่ไม่มี 3X, 4X...)")
            print(" ⚠️ ข้อสันนิษฐาน: Mechanical Looseness Type A ")
        else:
            print(" 💡 ตรวจพบ: 1X ล้วนๆ ในแนวรัศมี (H, V) โดยไม่มียอด 2X หรือ Order อื่นปะปนเลย")
            print(" ⚠️ ข้อสันนิษฐาน: Mass Unbalance (ไม่สมดุลมวลแบบ Force, Couple, Dynamic)")
            print(" ⚠️ เพิ่มเติม: ถ้าเช็คแล้วฐานมีอาการ (ขยับหรือบิดตัวนิดๆ) จะบอกว่าเป็น Looseness Type A")

# 7. หมวดความผิดปกติในแนวแกน (Angular Misalignment / Cocked Bearing / Bent Shaft)
# บังคับเด็ดขาด: ต้องมี 1X, 2X, หรือ 3X ในแกน A และ "ห้ามมี 1X, 2X, 3X ในแกน H และ V เลยแม้แต่ตัวเดียว"
elif (has_1x_a or has_2x_a or has_3x_a) and \
     not (has_1x_h or has_2x_h or has_3x_h or has_1x_v or has_2x_v or has_3x_v):
    
    # บังคับว่าต้องไม่มี Order อื่น (4X ขึ้นไป) มาปะปนในแกน A
    if not other_harm_a: 
        if has_3x_a:
            print(" 💡 ตรวจพบ: Order 1X, 2X, 3X เกิดขึ้นเฉพาะในแนวแกน (Axial) ล้วนๆ โดยไม่มีแกนรัศมี (H,V) หรือ Order อื่นมาปะปน")
            print(" ⚠️ ข้อสันนิษฐาน: Angular Misalignment (เยื้องศูนย์แบบเชิงมุม) หรือ Bearing Cocked on Shaft (ลูกปืนเอียงบนเพลา)")
            
        elif (max_order_a == 1.0 or max_order_a == 2.0):
            print(" 💡 ตรวจพบ: 1X และ/หรือ 2X โดดเด่นเป็นค่าสูงสุดในแนวแกน (Axial) โดยไม่มี Order อื่นรบกวน")
            print(" ⚠️ ข้อสันนิษฐาน: เป็นไปได้ทั้ง:")
            print("    - Angular Misalignment ")
            print("    - Bent Shaft (เพลาคด/งอ)")
    else:
        print(" 💡 ตรวจพบ: 1X, 2X, 3X ในแนวแกน (Axial) แต่มีฮาร์มอนิกที่สูงกว่า (4X ขึ้นไป) ปะปนอยู่ด้วย")
        print(" ⚠️ ข้อสันนิษฐาน: อาจเป็น Misalignment (เยื้องศูนย์รุนแรง) หรือ แท่นประกอบไม่ได้ระดับ")

# 8. ไม่เข้าเงื่อนไขใดเลย
else:
    print(" ❌ ไม่พบแพทเทิร์น Order ที่ตรงกับปัญหาพื้นฐาน")
    print(" ⚠️ ข้อสันนิษฐาน: เครื่องปกติ หรือ ตรวจสอบปัญหาจุดอื่น")

print("="*50 + "\n")