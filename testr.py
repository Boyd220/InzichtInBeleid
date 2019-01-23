    # Onderstaande handelingen zijn allemaal voorbereiding op basis waarvan de tweede oefening kan worden gedaan. # Het is in feite niks meer dan een herhaling van stappen uit de eerste oefening.

# Het inlezen van libraries
# Tidyverse libraries voor het werken met mooie (tidy) tabellen

library(tidyverse)
library(magrittr)

# Werken met datums
library(lubridate)

# Inlezen en SQL
library(sqldf)
library(haven)

# Data science libraries
library(sweep)
library(broom)
library(forecast)
library(timetk)
library(tidyquant)
library(modelr)

# Het bepalen van de werkdirectory (de map waar vandaan we bestanden inlezen en opslaan). Let op de dubbele "\" bij het ingeven van de locatie
setwd("U:\\IVA\\AI\\TONH\\R_WMO_oefeningen/")

# Inlezen van de data (dit is het via Slack bijgeleverde databestand) met de read.csv functie
HBH <- read.csv(file = "dummy_data.csv", sep = ",", stringsAsFactors = FALSE)

# Aanmaken van een nieuwe tabel met de begin- en einddatum, we veranderen ook direct het format van de variabelen naar een datum
HBH_datums_schoon <- HBH %>%
  select(DAT_BEGIN, DAT_EIND) %>%
  mutate(DAT_BEGIN = ymd(DAT_BEGIN),
         DAT_EIND = ymd(DAT_EIND)) %>%
  filter(!DAT_BEGIN > ymd("2017-01-01")) %>%
  filter(!DAT_EIND <= ymd("2012-01-01")) %>%
  filter(!DAT_EIND <= DAT_BEGIN)

# Aanmaken van een tijdserie
tijdserie <- seq(ymd("2012-01-01"),
                 ymd("2017-01-01"),
                 by = "1 month") %>%
  as.tibble() %>%
  select(DATUM = value)

# Voor het samenvoegen van de twee tabellen (de tijdserie en de tabel met begin- en einddata, gebruiken we de library sqldf, waarbij we met een SQL string een koppeling maken op de datums met BETWEEN
sql <- paste("SELECT a.*, b.*",
             "FROM tijdserie AS a LEFT JOIN HBH_datums_schoon AS b",
             "ON a.DATUM BETWEEN b.DAT_BEGIN AND b.DAT_EIND")

# De sql string gebruiken we om de nieuwe tabel te maken
indicaties_actief_per_datum <- sqldf(sql) %>% as.tibble()

# Vervolgens tellen we het aantal actieve indicaties per moment
HBH_tijdserie <- indicaties_actief_per_datum %>%
  group_by(DATUM) %>%
  summarize(AANTAL = n())

# Het resultaat van deze eerste bewerkingen
head(HBH_tijdserie)

# Hoe ziet onze data er ook alweer uit
HBH_tijdserie %>%
  ggplot(aes(x = DATUM, y = AANTAL)) +
  geom_point(alpha = .5) +
  geom_line(alpha = .2) +

  # Onderstaande is enkel voor de vormgeving
  ylim(1800, 2800) +
  labs(title = "Verloop van het aantal actieve indicaties HBH",
       subtitle = "Van 1 januari 2012 tot 1 januari 2017") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_tq() +
  scale_color_tq()

#Er is een functie die ons helpt om de data in drie elementen te ontleden.
#Deze functie heeft 'decompose' en de elementen zijn:
#.trend
#.seasonality
#.remainder

#Het idee is dat een ontwikkeling over tijd zich laat verklaren door het optellen (additive) of vermenigvuldigen (multiplicative) van deze drie elementen.
#Het ontleden werkt als volgt

# De data zetten we om naar een apart format, wat begrepen wordt door het model dat we gebruiken voor 'time series analysis'
HBH_ts <- tk_ts(HBH_tijdserie, start = 2012, end = 2017, frequency = 12)

# We maken een nieuw object aan met de decompose functie, we verkennen beide types
HBH_decomp <- decompose(HBH_ts, type = c("additive", "multiplicative"), filter = NULL)

# Dit object kunnen we gebruiken voor weergaven van de decompositie
autoplot(HBH_decomp) +
  theme_tq() +
  scale_color_tq()

# We nemen een deel van de volledige tijdserie om het model mee te trainen (tot 2016)
HBH_train <- tk_ts(HBH_tijdserie, start = 2012, end = 2016, frequency = 12)

# We maken een lijst aan met hierin het gewenste model (in ons geval auto.arima) en de parameters.
# Omdat auto.arima zelf zoekt naar de optimale parameters, hoeven we enkel de data (HBH_train) als parameter op te geven
models_list <- list(auto.arima = list(y = HBH_train))


# Vervolgens maken we een tabel met daarin een kolom met functies en een kolom met parameters
model_tbl <- enframe(models_list, name = "functie", value = "parameters")

# Dan maken we een aparte kolom aan met daarin de fit van het model
model_tbl %<>%
  mutate(fit = invoke_map(functie, parameters))

# Wat we nu hebben ziet er als volgt uit
model_tbl %>%
  mutate(glance = map(fit, sw_glance)) %>%
  unnest(glance, .drop = TRUE)

# We voegen de voorspelling toe met de forecast functie
model_tbl %<>%
  mutate(voorspelling = map(fit, forecast, h = 12))

# Met sweep voegen we een kolom toe waarin de uitwerking van de voorspelling terug te vinden is
model_tbl %<>%
  mutate(sweep = map(voorspelling, sw_sweep, fitted = FALSE, timetk_idx = TRUE, rename_index = "DATUM"))

# Het resultaat halen we terug met de 'unnest' functie
model_tbl %>%
  unnest(sweep) %>%

  # We zetten de kolommen even in een andere volgorde (vind ik wat logischer)
  select(functie, key, DATUM, AANTAL, everything())

# Eerst maken we een nette tabel aan met daarin de gewenste informatie
voorspelling_tbl <- model_tbl %>%
  unnest(sweep) %>%

  # We vullen de tabel aan met de daadwerkelijke cijfers voor 2017
  bind_rows(filter(HBH_tijdserie, DATUM >= ymd("2016-02-01"))) %>%

  # Omzetten van enkele termen
  mutate(key = replace(key, key == 'forecast', 'voorspelling'),
         key = replace(key, key == 'actual', 'verleden'),
         key = if_else(is.na(key), "werkelijkheid", key)) %>%

  # We maken een selectie en plaatsen het in een logische volgorde
  select(-functie) %>%
  select(key, DATUM, AANTAL, everything())

# Het resultaat
voorspelling_tbl

# Voor de grafiek gebruiken we onze tidy tabel voorspelling_tbl
voorspelling_tbl %>%

  # Opzetten van de grafiek, inclusief marges
  ggplot(aes(x = DATUM, y = AANTAL, color = key, group = key))  +
  geom_ribbon(aes(ymin = lo.95, ymax = hi.95),
              fill = "#D5DBFF", color = NA, size = 0, alpha = 0.2) +
  geom_ribbon(aes(ymin = lo.80, ymax = hi.80),
              fill = "#596DD5", color = NA, size = 0, alpha = 0.1) +
  geom_point(alpha = .5) +
  geom_line(alpha = .2) +

  # Onderstaande bepalingen voor een mooie weergave
  labs(title = "Aantal indicaties ten opzichte van werkelijkheid",
       subtitle = "Voorspelling met auto.arima",
       x = "", y = "Aantal") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  ylim(1800, 2800) +
  theme_tq() +
  scale_color_tq()

# We maken een nieuwe lijst met modellen, maar voegen dit keer alternatieve invullingen van ARIMA toe (parameters zijn willekeurig gekozen)
models_list_2 <- list(
  auto.arima = list(
    x = HBH_train
  ),

  # Hieronder staan de ARIMA modellen met zelf gekozen parameters
  arima = list(
    x = HBH_train,
    order = c(1,1,0),
    seasonal = list(order = c(0, 1, 0), period = 12)
  ),
  arima = list(
    x = HBH_train,
    order = c(0,1,0),
    seasonal = list(order = c(1, 1, 0), period = 12)
  ),
  arima = list(
    x = HBH_train,
    order = c(1,2,0),
    seasonal = list(order = c(0, 1, 0), period = 12)
  )
)

# Vervolgens herhalen we de stappen die we eerder hebben gedaan, met de pipe operator zetten we hier alle stappen direct onder elkaar
models_tbl_2 <-
  enframe(models_list_2, name = "functie", value = "parameters") %>%
  mutate(fit = invoke_map(functie, parameters),
         voorspelling = map(fit, forecast, h = 12),
         sweep = map(voorspelling, sw_sweep, fitted = FALSE, timetk_idx = TRUE, rename_index = "DATUM"),

         # Tot slot voegen we een benaming van de functies toe, dit gebruiken we later bij de visualisatie
         naam = c("auto.arima",
                  "arima(1,1,0)(0,1,0)",
                  "arima(0,1,0)(1,1,0)",
                  "arima(1,2,0)(0,1,0)"))

# Het resultaat met meerdere modellen is nu als volgt
models_tbl_2 %>%
  unnest(sweep)

# We maken een aparte tabel (voorspelling_tbl_2) aan om later mee te visualiseren
voorspelling_tbl_2 <- models_tbl_2 %>%
  unnest(sweep) %>%
  select(-functie) %>%

  # Toevoegen van de werkelijke aantallen (dit kan wellicht eenvoudiger) per functie. We doen dit per functie omdat dit ons helpt bij de visualisatie
  bind_rows(filter(HBH_tijdserie, DATUM >= ymd("2016-02-01"))) %>%
  mutate(naam = if_else(is.na(naam), "auto.arima", naam)) %>%
  bind_rows(filter(HBH_tijdserie, DATUM >= ymd("2016-02-01"))) %>%
  mutate(naam = if_else(is.na(naam), "arima(1,1,0)(0,1,0)", naam)) %>%
  bind_rows(filter(HBH_tijdserie, DATUM >= ymd("2016-02-01"))) %>%
  mutate(naam = if_else(is.na(naam), "arima(0,1,0)(1,1,0)", naam)) %>%
  bind_rows(filter(HBH_tijdserie, DATUM >= ymd("2016-02-01"))) %>%
  mutate(naam = if_else(is.na(naam), "arima(1,2,0)(0,1,0)", naam)) %>%

  # Omzetten van enkele termen
  mutate(key = replace(key, key == 'forecast', 'voorspelling'),
         key = replace(key, key == 'actual', 'verleden'),
         key = if_else(is.na(key), "werkelijkheid", key)) %>%

  # Netjes op volgorde zetten
  arrange(naam, key, DATUM)

# Het resultaat
voorspelling_tbl_2

# Grafiek maken we op basis van de tabel hierboven
voorspelling_tbl_2 %>%

  # Opzetten van de grafiek, het toevoegen van de marges werkt hier niet (na toevoeging van de werkelijke data uit 2016
  ggplot(aes(x = DATUM, y = AANTAL, color = key)) +
  geom_point(alpha = .5) +

  # Onderstaande bepalingen hebben te maken met enkele voorkeuren voor de weergave
  facet_wrap(~naam, ncol = 2) +
  labs(title = "Aantal indicaties ten opzichte van de werkelijkheid",
       subtitle = "Voorspellen en vergelijken met ARIMA",
       x = "", y = "AANTAL") +
  scale_x_date(date_breaks = "1 years", date_labels = "%Y") +
  ylim(1700, 2800) +
  theme_tq() +
  scale_color_tq()

# Met enkele bewerkingen van voorspelling_tbl_2 berekenen we meetwaarden
# NB: leuk om de stappen één voor één uit te voeren en te zien wat elke stap doet
voorspelling_tbl_2 %>%
  filter(key %in% c("voorspelling", "werkelijkheid")) %>%
  select(naam, DATUM, key, AANTAL) %>%
  arrange(naam, DATUM) %>%
  spread(key, AANTAL) %>%
  group_by(naam) %>%
  summarize(RMSE = rmse(werkelijkheid, voorspelling),
            MAE = mae(werkelijkheid, voorspelling),
            MAPE = mape(werkelijkheid, voorspelling),
            MASE = mase(werkelijkheid, voorspelling)) %>%
  arrange(RMSE)
