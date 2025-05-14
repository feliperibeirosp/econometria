
pacman::p_load(dplyr, forecast, fpp3)

aus_holidays <- tourism %>%
  filter(Purpose == "Holiday") %>%
  summarise(Trips = sum(Trips)/1e3)

fit <- aus_holidays %>%
  model(
    additive = ETS(Trips ~ error("A") + trend("A") +
                     season("A")),
    multiplicative = ETS(Trips ~ error("M") + trend("A") +
                           season("M"))
  )

fc <- fit %>% forecast(h = "3 years")

fc %>%
  autoplot(aus_holidays, level = NULL) +
  labs(title="Turismo doméstico Austrália",
       y="Viagens noturnas (millions)", 
       x = 'Trimestres') +
  guides(colour = guide_legend(title = "Forecast"))
