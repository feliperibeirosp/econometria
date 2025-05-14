import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.exponential_smoothing.ets import ETSModel

# Simulando dados (em R você usa tourism do fpp3)
# Aqui vamos simular um DataFrame semelhante
# Se você tiver o dataset original em CSV ou outra forma, posso ajustar
# Exemplo de simulação:
dates = pd.date_range(start="2000-01-01", periods=80, freq="Q")
import numpy as np
np.random.seed(0)
data = pd.DataFrame({
    "Quarter": dates,
    "Purpose": ["Holiday"] * 80,
    "Trips": 1000 + 100 * np.sin(np.linspace(0, 12 * np.pi, 80)) + np.random.normal(0, 50, 80)
})

# Filtro apenas para "Holiday"
aus_holidays = data[data["Purpose"] == "Holiday"].copy()

# Agrupando e somando viagens (dividindo por 1e3)
aus_holidays = aus_holidays.groupby("Quarter", as_index=False)["Trips"].sum()
aus_holidays["Trips"] = aus_holidays["Trips"] / 1e3

# Ajustando modelos ETS aditivo e multiplicativo
# Você pode usar a coluna Quarter como índice
aus_holidays.set_index("Quarter", inplace=True)

# Modelo ETS aditivo
model_add = ETSModel(aus_holidays["Trips"], error="add", trend="add", seasonal="add", seasonal_periods=4)
fit_add = model_add.fit()

# Modelo ETS multiplicativo
model_mul = ETSModel(aus_holidays["Trips"], error="mul", trend="add", seasonal="mul", seasonal_periods=4)
fit_mul = model_mul.fit()

# Previsão para 3 anos (12 trimestres)
forecast_add = fit_add.forecast(steps=12)
forecast_mul = fit_mul.forecast(steps=12)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(aus_holidays.index, aus_holidays["Trips"], label="Observado")
plt.plot(forecast_add.index, forecast_add, label="Aditivo (ETS)", linestyle="--")
plt.plot(forecast_mul.index, forecast_mul, label="Multiplicativo (ETS)", linestyle="--")
plt.title("Turismo doméstico Austrália")
plt.xlabel("Trimestres")
plt.ylabel("Viagens noturnas (milhões)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()