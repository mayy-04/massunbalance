# =========================================================
# 1. ข้อมูลนำเข้า (Input Data) - ชุดข้อมูลทดสอบ Bent Shaft
# =========================================================
# ข้อมูลความถี่ (Hz) 
f_point_h = [22.0, 10.0, 58.0, 27.0, 28.0, 36.0, 49.0, 56.0, 68.0, 77.0]
f_point_v = [27.0, 10.0, 62.0, 28.0, 29.0, 37.0, 42.0, 54.0, 67.0, 74.0]
f_point_a = [10.0, 20.0, 34.0, 46.0, 50.0, 60.0, 70.0, 89.0, 93.0, 83.0]

# ข้อมูลความเร็ว (mm/s) 
v_h_data = [50.0, 40.0, 45.0, 70.0, 35.0, 20.0, 10.0, 5.0, 5.0, 2.0]
v_v_data = [45.0, 35.0, 40.0, 25.0, 30.0, 15.0, 8.0, 4.0, 4.0, 1.5]
v_a_data = [5.0, 4.0, 3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0, 0.5]

rpm = 600 # round per minute

# =========================================================
# 2. การคำนวณและแปลงความถี่เป็น Order (Calculations)
# =========================================================
running_speed_hz = rpm / 60.0  # 600 / 60 = 10.0 Hz (1X หรือ Order 1)

# แปลงความถี่ทุกตัวให้เป็น Order (ปัดเศษ 2 ตำแหน่ง) และตัดค่าซ้ำด้วย set() เพื่อใช้เช็คเงื่อนไข
order_h = [round(val / running_speed_hz, 2) for val in f_point_h]
order_v = [round(val / running_speed_hz, 2) for val in f_point_v]
order_a = [round(val / running_speed_hz, 2) for val in f_point_a]

set_order_h = set(order_h)
set_order_v = set(order_v)
set_order_a = set(order_a)

# --- หาค่าสูงสุด (Max) ---
max_val_h = max(v_h_data)
max_index_h = v_h_data.index(max_val_h)
f_at_max_h = f_point_h[max_index_h]

max_val_v = max(v_v_data)
max_index_v = v_v_data.index(max_val_v)
f_at_max_v = f_point_v[max_index_v]

max_val_a = max(v_a_data)
max_index_a = v_a_data.index(max_val_a)
f_at_max_a = f_point_a[max_index_a]

# =========================================================
# 3. แสดงผลลัพธ์และการวิเคราะห์ (Outputs)
# =========================================================
print(" 📊 สรุปค่าสูงสุด (Max)")
print("=======================================================")
print(f"🟢  แกน HORIZONTAL : Max = {max_val_h} mm/s ที่ความถี่ {f_at_max_h} Hz (Order {round(f_at_max_h/running_speed_hz, 2)})")
print(f"🔵  แกน VERTICAL   : Max = {max_val_v} mm/s ที่ความถี่ {f_at_max_v} Hz (Order {round(f_at_max_v/running_speed_hz, 2)})")
print(f"🟣  แกน AXIAL      : Max = {max_val_a} mm/s ที่ความถี่ {f_at_max_a} Hz (Order {round(f_at_max_a/running_speed_hz, 2)})")

print(f"\n=======================================================")
print(f" ⚙️ สรุปค่า Order ที่พบในระบบแบบแยกแกน (1X = {running_speed_hz} Hz)")
print(f"=======================================================")
print(f"Order แกน HORIZONTAL (H) : {sorted(list(set_order_h))}")
print(f"Order แกน VERTICAL (V)   : {sorted(list(set_order_v))}")
print(f"Order แกน AXIAL (A)      : {sorted(list(set_order_a))}")

print(f"\n=======================================================")
print(f" 🎯 วิเคราะห์ปัญหาตาม Diagnostic Chart (รวมอาการที่ Spectrum ซ้ำกัน)")
print(f"=======================================================")

# --- เตรียมตัวแปรเช็คเงื่อนไขแยกตามแกน H, V และ A ---
has_1x_h = 1.0 in set_order_h
has_1x_v = 1.0 in set_order_v
has_1x_a = 1.0 in set_order_a

has_2x_a = 2.0 in set_order_a

oil_whirl_h = [o for o in set_order_h if 0.40 <= o <= 0.48]
oil_whirl_v = [o for o in set_order_v if 0.40 <= o <= 0.48]

harmonics_h = [o for o in set_order_h if o in [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]
harmonics_v = [o for o in set_order_v if o in [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]

fractional_h = [o for o in set_order_h if o % 1 == 0.5]
fractional_v = [o for o in set_order_v if o % 1 == 0.5]

# --- เริ่มการวินิจฉัย ---
if oil_whirl_h or oil_whirl_v:
    print("✅ ผลลัพธ์: พบ Order ในช่วง 0.40X - 0.48X ในแนวรัศมี")
    if oil_whirl_h: print(f"   - แกน H พบ: {sorted(oil_whirl_h)}")
    if oil_whirl_v: print(f"   - แกน V พบ: {sorted(oil_whirl_v)}")
    print("🔍 [ข้อสันนิษฐาน]: Oil Whirl Instability")

elif fractional_h or fractional_v:
    print(f"✅ ผลลัพธ์: พบความถี่เศษส่วน (0.5X, 1.5X...) ในแนวรัศมี")
    if fractional_h: print(f"   - แกน H พบ: {sorted(fractional_h)}")
    if fractional_v: print(f"   - แกน V พบ: {sorted(fractional_v)}")
    print("🔍 [ข้อสันนิษฐาน]: เป็นไปได้ทั้งอาการต่อไปนี้ เนื่องจากมี Spectrum คล้ายกัน:")
    print("   - Rotor Rub (โรเตอร์เสียดสี)")
    print("   - Mechanical Looseness Type C (ความหลวมจากการสวมประกอบ)")

elif (harmonics_h or harmonics_v) and (has_1x_h or has_1x_v):
    print(f"✅ ผลลัพธ์: พบความถี่ 1X ร่วมกับความถี่ฮาร์มอนิกเต็มหน่วยอื่นๆ ในแนวรัศมี")
    if harmonics_h: print(f"   - แกน H พบ Harmonic: {sorted(harmonics_h)}")
    if harmonics_v: print(f"   - แกน V พบ Harmonic: {sorted(harmonics_v)}")
    print("🔍 [ข้อสันนิษฐาน]: เป็นไปได้ทั้งอาการต่อไปนี้ เนื่องจากมี Spectrum คล้ายกัน:")
    print("   - Mechanical Looseness Type B (หรือ Type C ในบางกรณี)")
    print("   - Journal Bearings Wear (แบริ่งกาบสึกหรอ)")

elif has_1x_h and has_1x_v:
    if has_1x_a:         
        print("✅ ผลลัพธ์: พบ Order 1X ครบทั้งแนวรัศมี (H, V) และแนวแกน (A)")
        print("🔍 [ข้อสันนิษฐาน]: Overhung Rotor Unbalance (โรเตอร์ยื่นมีความไม่สมดุล)")
    else:
        print("✅ ผลลัพธ์: พบ Order 1X เฉพาะในแนวรัศมี (H หรือ V) โดยไม่มีฮาร์มอนิกอื่นปน")
        print("🔍 [ข้อสันนิษฐาน]: เป็นไปได้ทั้งอาการต่อไปนี้ เนื่องจากมี Spectrum เป็น 1X เหมือนกันทั้งหมด:")
        print("   - Mass Unbalance (Force, Couple หรือ Dynamic)")
        print("   - Mechanical Looseness Type A (ฐานเครื่องหรือโครงสร้างหลวม)")

# --- เงื่อนไข Bent Shaft ---
elif has_1x_a and has_2x_a:
    print("✅ ผลลัพธ์: พบความถี่ 1X และ/หรือ 2X โดดเด่นเฉพาะในแนวแกน (Axial)")
    print("🔍 [ข้อสันนิษฐาน]: Bent Shaft (เพลาคด/งอ)")

else:
    print("❌ ผลลัพธ์: ไม่พบแพทเทิร์น Order ที่ตรงกับปัญหาพื้นฐานในตาราง")
    print("🔍 [ข้อสันนิษฐาน]: ให้ตรวจสอบปัญหาในหมวดอื่นๆ ")
