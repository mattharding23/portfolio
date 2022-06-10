#### Script Explanation:
# Data Wrangling: Various csv files holding data specific to XC Teams will be accessed and combined into a working df
# This working dataframe will have the team as the unit of interest
# Visualization: An interactive plotly visualization will be created from the resulting df
# This viz will be specific to each teams relative success/challenges when racing in different weather conditions
# Weather data collected from: weatherspark.com


#### Loading necessary libraries ####
library(tidyr)
library(dplyr)
library(ggplot2)
library(plotly)
library(htmlwidgets)
devtools::install_version("crosstalk", version = "1.1.1")
library(crosstalk)
library(htmltools)


#### Accessing Data ####
ranking_data <- read.csv("Data/Ranking_Data/updated_xc_rank.csv")
weather_data <- read.csv("Data/Weather_Data/raceDay_weatherConditions.csv", fileEncoding = "UTF-8-BOM")


#### Filtering weather data to only have four weather conditions: wind, sun, snow, rain ####
filtered_weather_data <-
  weather_data %>%
  filter(Year == "2017" | Year == "2018" | Year == "2019" | Year == "2021")


#### Merging weather data with ranking_data ####
weather_merge <- left_join(ranking_data, filtered_weather_data)


#### Removing data that is not weather dependent ####
weather_merge <-
  weather_merge %>%
  filter_at(vars(Weather_Condition), all_vars(!is.na(.)))


#### Converting Gender Column to type factor ####
weather_merge$Gender = as.factor(weather_merge$Gender)


#### Adjusting Rank Variable from placement at nationals to 32 minus placement at nationals ####
weather_merge$Rank <- 32 - weather_merge$Rank


#### Create highlight key for visual ####
key <- highlight_key(weather_merge, ~ row.names(weather_merge))


#### Create adjustable widgets ####
widgets <- bscols(
  widths = c(12, 12, 6, 6),
  ## Add title and theme
  div("Impact of Weather on Team Performance", style = css(width = "100%", height = "100%", background_color = "linen", font.family = "Verdana", font.weight = "bold", text.align = "center", font.size = "18px")),
  div("Team Performance Score Scale: 31 Strongest - 1 Weakest", style = css(width = "100%", height = "100%", background_color = "linen", font.family = "Verdana", text.align = "center", font.size = "12px")),
  ## Add Selection by gender
  filter_select(
    id = "Gender",
    label = "Select Gender",
    sharedData = key,
    group = ~Gender,
    multiple = F, # Can only select one gender at a time
    allLevels = F
  ) %>% div(style = css(width = "100%", height = "100%", font.family = "Verdana")),
  ## Add filter by team
  filter_select(
    id = "Team",
    label = "Select Team(s)",
    sharedData = key,
    group = ~Team
  ) %>% div(style = css(width = "100%", height = "100%", font.family = "Verdana"))
)

#### Creating A Radar Chart for Men and Women ####
radar <- plot_ly(key,
  type = "scatterpolar", # Radar Chart
  r = ~Rank, # Plotted points from Rank column
  theta = ~Weather_Condition, # theta is the weather condition
  fill = "toself",
  fillcolor = ~Team, # Coloring by team
  hovertemplate = ~ paste(
    paste("Team Performance Score: ", Rank),
    paste("Year of Race: ", Year),
    sep = "<br />"
  ) # Adjusting tooltip text displayed
)

## Formatting layout of radar plot
radar <- radar %>%
  layout(
    polar = list(
      radialaxis = list(
        visible = T,
        range = c(0, 31)
      )
    )
  )

## Adding radar plot to widget
radar <- bscols(
  widths = c(12, 12),
  widgets,
  radar
)

## Display
radar

#### Saving visuals as a html files ####
htmltools::save_html(radar, "Visuals/Weather_Visual/weather_radarChart.html")

