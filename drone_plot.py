import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Inputs
# ----------------------------
rho = 1.225          # [kg/m^3] air density
g = 9.81             # [m/s^2]

# Wing geometry
chord = 0.25         # [m]
AR = 7.44             # [-]
b = AR * chord       # [m] rectangular wing assumption
print(f"Wingspan b         : {b:.3f} m")
S = b * chord        # [m^2]

# Aerodynamics
CL_max = 1.4         # [-]
CD0 = 0.05          # [-]
e = 0.80             # [-]
k = 1.0 / (np.pi * e * AR)

# Design speed for full-size glider
V_release = 33.3     # [m/s]

# ----------------------------
# Derived best-glide quantities
# ----------------------------
CL_star = np.sqrt(CD0 / k)                   # CL for max L/D
LD_max = 1.0 / (2.0 * np.sqrt(CD0 * k))      # maximum L/D

print("---- Derived quantities ----")
print(f"Wing area S        : {S:.4f} m^2")
print(f"Induced factor k   : {k:.5f}")
print(f"CL* for max L/D    : {CL_star:.3f}")
print(f"(L/D)_max          : {LD_max:.2f}")

# ============================================================
# FIGURE 1: Stall speed vs total mass (prototype feasibility)
# ============================================================
masses = np.linspace(0.5, 16.0, 200)   # [kg], adjust as needed
weights = masses * g

Vs = np.sqrt((2.0 * weights) / (rho * S * CL_max))

plt.figure(figsize=(8, 5))
plt.plot(masses, Vs, label=r"Stall speed $V_s$")
plt.axhline(6.0, linestyle="--", label="Lower hand-launch target (6 m/s)")
plt.axhline(10.0, linestyle="--", label="Upper hand-launch target (10 m/s)")

plt.xlabel("Total mass [kg]")
plt.ylabel("Stall speed [m/s]")
plt.title("Prototype feasibility: Stall speed versus total mass")
plt.grid(True)
plt.legend()
plt.tight_layout()
#plt.show()

# ============================================================
# FIGURE 2: Mass-speed envelope for final glider
# ============================================================
V = np.linspace(5.0, 45.0, 400)   # [m/s]

# Maximum mass supportable without stalling at each speed
m_stall = (0.5 * rho * V**2 * S * CL_max) / g

# Mass that corresponds to flying exactly at CL* (best glide)
m_best_glide = (0.5 * rho * V**2 * S * CL_star) / g

CL_alpha1 = 0.5
m_CL05 = (0.5 * rho * V**2 * S * CL_alpha1) / g

# Value at release speed
m_release_best_glide = (0.5 * rho * V_release**2 * S * CL_star) / g
m_release_stall = (0.5 * rho * V_release**2 * S * CL_max) / g
m_release_CL05 = (0.5 * rho * V_release**2 * S * CL_alpha1) / g


plt.figure(figsize=(8, 5))
#plt.plot(V, m_stall, label=r"Stall boundary ($C_L = C_{L\max}$)")
plt.plot(V, m_best_glide, label=r"Best-glide curve ($C_L = C_{L*}$)")
plt.plot(V, m_CL05, label="CL at α = 1° (CL = 0.5)")
plt.axvline(V_release, linestyle="--", label=f"Design release speed = {V_release:.1f} m/s")

plt.scatter([V_release], [m_release_best_glide], zorder=5)
#plt.scatter([V_release], [m_release_stall], zorder=5)
plt.scatter([V_release], [m_release_CL05], zorder=5)

plt.annotate(
    f"Best glide mass at {V_release:.1f} m/s:\n{m_release_best_glide:.2f} kg",
    xy=(V_release, m_release_best_glide),
    xytext=(V_release + 1.0, m_release_best_glide + 0.3),
    arrowprops=dict(arrowstyle="->")
)

#plt.annotate(
#    f"Stall limit at {V_release:.1f} m/s:\n{m_release_stall:.2f} kg",
#    xy=(V_release, m_release_stall),
##    xytext=(V_release - 12.0, m_release_stall + 0.6),
 #   arrowprops=dict(arrowstyle="->")
#)

plt.annotate(
    f"$C_L(1^\\circ)=0.5$:\n{m_release_CL05:.2f} kg",
    xy=(V_release, m_release_CL05),
    xytext=(V_release + 1.0, m_release_CL05 - 0.8),
    arrowprops=dict(arrowstyle="->")
)

plt.xlabel("Airspeed [m/s]")
plt.ylabel("Total mass [kg]")
plt.title("Final glider feasibility envelope")
plt.grid(True)
plt.legend()
plt.tight_layout()
#plt.show()

# ============================================================
# OPTIONAL: Glide ratio and sink rate vs speed for chosen masses
# ============================================================
mass_cases = [2.0, 4.0, 16.0]   # [kg], example values
plt.figure(figsize=(8, 5))

for m in mass_cases:
    W = m * g
    q = 0.5 * rho * V**2
    CL_req = W / (q * S)
    CD_req = CD0 + k * CL_req**2
    LD = CL_req / CD_req

    # Mask region below stall
    LD_masked = np.where(CL_req <= CL_max, LD, np.nan)
    plt.plot(V, LD_masked, label=f"{m:.1f} kg")

plt.xlabel("Airspeed [m/s]")
plt.ylabel("Lift-to-drag ratio L/D [-]")
plt.title("Glide ratio versus speed for selected total masses")
plt.grid(True)
plt.legend(title="Mass")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))

for m in mass_cases:
    W = m * g
    q = 0.5 * rho * V**2
    CL_req = W / (q * S)
    CD_req = CD0 + k * CL_req**2
    LD = CL_req / CD_req
    sink_rate = V / LD

    # Mask region below stall
    sink_masked = np.where(CL_req <= CL_max, sink_rate, np.nan)
    plt.plot(V, sink_masked, label=f"{m:.1f} kg")

plt.xlabel("Airspeed [m/s]")
plt.ylabel("Sink rate [m/s]")
plt.title("Sink rate versus speed for selected total masses")
plt.grid(True)
plt.legend(title="Mass")
plt.tight_layout()
plt.show()
