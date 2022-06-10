#### Loading necessary libraries ####
# library(maps)
library(tidyr)
library(dplyr)
library(ggplot2)
library(plotly)
library(htmlwidgets)
library(htmltools)
library(crosstalk)

#### Accessing Data ####
df <- read.csv("Data/Ranking_Data/team_caliber.csv")
df = na.omit(df)

#### Bin altitude into two groups.
#### According to the Army Public Health Center: Moderate altitude is considered at 4,000 ft and above. Therefore, the threshold will be at 4,000. High altitude is considered
### Max of 7234 for men and 6893 both lie within range of 7300 or less
df <- df %>% mutate(elevation_group = cut(elevation, breaks = c(0,4000,7300), labels = c("Low Altitude", "High Altitude")))

#### Defining variables for visualization ####
## Styling the Geographic Area being displayed
# Will result in graph of only the USA
geo <- list(
  scope = "usa",
  projection = list(type = "albers usa"),
  showland = TRUE,
  showlakes = TRUE,
  showcountries = FALSE,
  lakecolor = toRGB("white"), #FAF0E6
  landcolor = toRGB("grey90"),
  subunitcolor = toRGB("white"),
  countrycolor = toRGB("grey15"),
  coastlinecolor = toRGB("black"),
  countrywidth = 0.5,
  subunitwidth = 0.5,
  bgcolor = toRGB('white') #FAF0E6
)


#### Creating XC Men's Teams Visualization ####
## Create adjustable widgets
## Create highlight key
key <- highlight_key(df, ~row.names(df))

## Create widget with filters
widgets <- bscols(
  widths = c(12, 12, 6, 6),
  #Add title and theme
  div("Impact of Altitude on Team Performance", style = css(width = "100%", height = "100%", background_color="linen", font.family = "Verdana", font.weight = "bold", text.align = "center", font.size = "18px")),
  div("(Hover for info)", style = css(width = "100%", height = "100%", background_color="linen", font.family = "Verdana", text.align = "center", font.size = "12px")),
  #Add Checkbox by gender
  filter_select("Gender", "Select Gender", key, ~Gender) %>% div(style = css(font.family = "Verdana")),
  #Add filter by team
  filter_select("Altitude", "Select Altitude(s)", key, ~elevation_group) %>% div(style = css(font.family = "Verdana")))


## Creating geographic plot
fig <- plot_geo(key, lat = ~lat, lon = ~long, stroke = I("black"))
## Adding markers and hover stats.
fig <- fig %>% add_markers(
  text = ~ paste(
    paste("School: ", Team),
    paste("Elevation: ", elevation, "ft"),
    paste("NCAA Appearances in 11 Years: ", Appearances, "appearance(s)"),
    paste("Average Performance Placement: ", Average_Placement),
    sep = "<br />"
  ),
  color = ~-Average_Placement,
  symbol = I("circle"),
  size = I(40),
  hoverinfo = "text",
  colors = "Blues"
)
## Adding viz title and defining the geographic region to display
fig <- fig %>% layout(
  paper_bgcolor = toRGB('white'), #FAF0E6
  geo = geo
) %>% hide_colorbar()

widgetfig <- bscols(
  widths = c(9, 2),
  fig,
  div(img(src="colorbar.png", height = "200px")) #colorbarbeige.png
)
## Displaying the figure for the XC  Teams
select_figure = bscols(
  widths = c(12, 12),
  widgets,
  widgetfig)

select_figure
#### Saving visuals as a html files ####
htmltools::save_html(select_figure, "Visuals/Altitude_Visual/altitude_dependent.html")
