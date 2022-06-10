####################################
## Create linked view
####################################

### Load in libraries
library(tidyverse)
library(plotly)
library(htmlwidgets)
library(crosstalk)
library(htmltools)


### Read in dataframe
df <- read.csv("Data/Ranking_Data/updated_xc_rank.csv")

## Create highlight key
df <- df %>% unite("TeamGender", c("Team","Gender"), sep = " ", remove = FALSE)
key <- highlight_key(df, ~TeamGender)
#key <- highlight_key(df, ~Team)
## Create adjustable widgets
widgets <- bscols(
  widths = c(12, 12, 6, 6), #Each division needs to have a width of 12
  #Add title and theme
  #Theme is linen with additional css styling
  div("Impact of Ranking Change on Team Performance", style = css(width = "100%", height = "100%", background_color="linen", font.family = "Verdana", font.weight = "bold", text.align = "center", font.size = "18px")),
  div("(Hover for info)", style = css(width = "100%", height = "100%", background_color="linen", font.family = "Verdana", text.align = "center", font.size = "12px")),
   #Add Checkbox by gender
  filter_select("Gender", "Select Gender", key, ~Gender) %>% div(style = css(width = "100%", height = "100%", font.family = "Verdana")),
  #Add filter by team
  filter_select("Team", "Select Team(s)", key, ~Team) %>% div(style = css(width = "100%", height = "100%", font.family = "Verdana"))
  )

# Create visual with widgets
visual <-bscols(
  widths = c(12, 6, 6), widgets, #Each division needs to have a width of 12.
  #Create scatter plot of performances
  plot_ly(key, x = ~Year, y = ~Change, showlegend = FALSE, text = ~TeamGender, hovertemplate = paste(
    "<b>%{text}</b><br><br>",
    "%{yaxis.title.text}: %{y:}<br>",
    "%{xaxis.title.text}: %{x:}<br>",
    "<extra></extra>")) %>%
    #Add markers and conditional color for Change value at a threshold of 0.
    add_markers(color = ~Change < 0, colors = c("dark green", "red")) %>%
    #Add title and create general theming with linen color and title labels
    layout(title = "",
           xaxis = list(color = '#000000',
                        tickangle = -45),
           yaxis = list(color = '#000000', title = "Ranking Change"),
           title = "Team Attendances",
           titlefont = list(family = "Verdana",
                            size = 30,
                            color = '#000000'),
           font = list(family = "Verdana",
                       size = 15),
           margin = 10,
           legend = list(font=list(color = '#000000'))),
  #Create histogram of performances for linking
  plot_ly(key, x = ~Year, y = ~Change, showlegend = FALSE, hovertemplate = paste(
    "%{yaxis.title.text}: %{y:}<br>",
    "<extra></extra>")) %>%
    #Add markers and conditional color
    add_histogram(y = ~Change, color = ~Change < 0, colors = c("dark green", "red")) %>%
    #Add title and create general theming with linen color and title labels
    layout(title = "",
           xaxis = list(color = '#000000',
                        tickangle = -45,
                        title = 'Frequency'),
           yaxis = list(color = '#000000',
                        title = 'Ranking Change'),
           title = "Team Attendances",
           titlefont = list(family = "Verdana",
                            size = 30,
                            color = '#000000'),
           font = list(family = "Verdana",
                       size = 15),
           margin = 10,
           legend = list(font=list(color = '#000000'))))

visual
#### Saving visuals as a html files
htmltools::save_html(visual, "Visuals/Change_Previous_Rank_Visual/change_scatter_histogram.html")
