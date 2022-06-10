####################################
## Create pie charts of podium teams
####################################

### Load in libraries
library(stringr)
library(tidyverse)
library(plotly)
library(htmlwidgets)

### Read in dataframe
df <- read.csv("Data/Ranking_Data/updated_xc_rank.csv")

### Subset rank
df_men <- df %>% filter(Gender == "Men" & Rank %in% c(1, 2, 3, 4))
df_women <- df %>% filter(Gender == "Women" & Rank %in% c(1, 2, 3, 4))

### Group by team and summarize points and Rank
df_men <- df_men %>%
  select(Team, Points, Rank) %>%
  group_by(Team) %>%
  add_count(Team) %>%
  summarize(across(everything(), mean))

df_women <- df_women %>%
  select(Team, Points, Rank) %>%
  group_by(Team) %>%
  add_count(Team) %>%
  summarize(across(everything(), mean))

## Remove teams who only podium once. These teams are less important to understanding top teams in the NCAA.
## This helps reduce teams
df_men = df_men %>% filter(n > 2)
df_women = df_women %>% filter(n > 2)

## Manually remove Michigan and Providence to have an even number of teams represented
df_women = df_women %>% filter(Team != c("MICHIGAN"))
df_women = df_women %>% filter(Team != c("PROVIDENCE"))

## Round numbers
df_men<- df_men %>% mutate_at(vars(Points, Rank), ~round(.,1))
df_women <- df_women %>% mutate_at(vars(Points, Rank), ~round(.,1))

## Create vertical line
vline <- function(x = 0, color = "black") {
  list(
    type = "line",
    y0 = 0,
    y1 = 1,
    yref = "paper",
    x0 = x,
    x1 = x,
    line = list(color = color, dash="dot")
  )
}

## Create plotly object
fig <- plot_ly()
fig <- fig %>% add_pie(data = df_men, labels = ~Team, values = ~n, name = "Men", textinfo = "none", hoverinfo = "text", text = ~ paste("Men","\n", Team, "\n", n, "NCAA Podium Placement(s)", "\n", "Average Podium Placement:", Rank), title = "Men", domain = list(x = c(0, 0.45), y = c(0, 1)))
fig <- fig %>% add_pie(data = df_women, labels = ~Team, values = ~n, name = "Women", textinfo = "none", hoverinfo = "text", text = ~ paste("Women","\n", Team, "\n", n, "NCAA Podium Placement(s)", "\n", "Average Podium Placement:", Rank), title = "Women", domain = list(x = c(0.55, 1), y = c(0, 1)))
fig <- fig %>% layout(
  title = ~paste("<b>Top 6 Significant Performing Men's", "\n", "and Women's Cross Country Teams","</b>"),
  showlegend = T,
  paper_bgcolor='#FAF0E6',
  plot_bgcolor='#FAF0E6',
  xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
  yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
  titlefont = list(family = "Verdana",
                   size = 25,
                   color = '#000000'),
  font = list(family = "Verdana",
              size = 20),
  margin = 10,
  legend = list(font = list(size = 10)),
  shapes = list(vline(0.5))
)

fig


#### Saving visuals as a html files
htmlwidgets::saveWidget(as_widget(fig), "Visuals/Top_6_Team_Visual/podium_performances.html")
