def calculate_physics(m, F, mu, v, x, dt=0.016):
    """
    Core engine fisika 1D (v1.2 - Stable)
    - Fix arah vektor gesekan
    - Guard untuk massa = 0
    - Clamp untuk stabilitas floating point
    """
    # 1. GUARD: Mencegah ZeroDivisionError dan fisika tidak logis
    if m <= 0:
        raise ValueError("Massa harus lebih besar dari 0")
        
    g = 9.8
    F_friction_max = mu * m * g
    
    # 2. VEKTOR GESEKAN: Selalu melawan arah gerak atau arah dorongan
    if abs(v) > 0.001:
        F_friction = -F_friction_max * (1 if v > 0 else -1)
    else:
        F_friction = -F_friction_max * (1 if F > 0 else -1)

    # 3. EVALUASI STATE: Tertahan gaya gesek statis
    if abs(F) <= F_friction_max and abs(v) <= 0.01:
        F_friction = -F  # Gesekan statis menyesuaikan gaya dorong
        F_net = 0.0
        a = 0.0
        v = 0.0
    else:
        # 4. KALKULASI DINAMIS
        F_net = F + F_friction
        a = F_net / m
        v_next = v + a * dt
        
        # 5. KONTROL DESELERASI: Cegah gerak mundur (jitter) saat berhenti
        if F == 0 and (v * v_next) <= 0:
            v = 0.0
            a = 0.0
        else:
            v = v_next

    # 6. CLAMPING: Membersihkan sisa angka mikroskopis (floating point noise)
    if abs(v) < 1e-5:
        v = 0.0
        
    # 7. UPDATE SPASIAL & ENERGI
    x = x + v * dt
    Ek = 0.5 * m * (v ** 2)
    
    # Output lengkap agar UI bisa merender semua komponen vektor
    return F_net, F_friction, a, v, x, Ek