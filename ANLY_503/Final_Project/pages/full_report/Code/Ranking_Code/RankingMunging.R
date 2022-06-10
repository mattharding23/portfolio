######
## Clean up raw data
#####

### Read in library
library(stringr)
library(tidyverse)

### Read in dataframe
df <- read.csv("Data/Ranking_Data/xc_rank.csv")

### Replace Receiving Votes with NR
df$Change[df$Change == "(LW: RV)"] <- "NR"

### Split column
split <- str_split_fixed(df$Change, "\\(", 2)
df$Change <- split[, 1]
df$`Previous Rank` <- split[, 2]

### Remove arrows
df$Change <- gsub("◀▶", 0, df$Change)
df$Change <- gsub("▲", "", df$Change)
df$Change <- gsub("▼", "-", df$Change)

### Add NR to Previous Rank Column
df$`Previous Rank` <- gsub("LW:", "", df$`Previous Rank`)
df$`Previous Rank` <- gsub("\\)", "", df$`Previous Rank`)
df$`Previous Rank`[df$Change == "NR"] <- df$Change[df$Change == "NR"]

### Calculate change (31-Current Rank)
df$`Previous Rank` <- gsub("NR", 32, df$`Previous Rank`) # Replace Unranked with 32
df$`Previous Rank` <- as.numeric(df$`Previous Rank`)
df$ChangeNew <- (df$`Previous Rank` - df$Rank)

## Add Categorical
df$`Previous Ranking Class` <- "Ranked"
df$`Previous Ranking Class`[df$Change == "NR"] <- df$Change[df$Change == "NR"]
df$`Previous Ranking Class`[df$`Previous Ranking Class` == "NR"] <- "Unranked"

## Reorder Dataframe
df <- df[c(1:4, 12, 11, 13, 6:10)]

## Rename New Change
df <- df %>% rename(Change = ChangeNew)

## Save csv
write.csv(df, "Data/Ranking_Data/updated_xc_rank.csv", row.names = FALSE)


#########
### Part 2 -- Find average across teams & combine with elevation data
#########

# ## Subset dataframe by men's teams and women's teams
df_men <- df %>% filter(Gender == "Men")
df_women <- df %>% filter(Gender == "Women")

## Compute average rank
df_men <- df_men %>%
  select(Rank, Team, Gender) %>%
  group_by(Team, Gender) %>%
  add_count(Team) %>%
  summarize(across(everything(), mean))

df_women <- df_women %>%
  select(Rank, Team, Gender) %>%
  group_by(Team, Gender) %>%
  add_count(Team) %>%
  summarize(across(everything(), mean))

## Rename as average
df_men <- rename(df_men, Average_Placement = Rank, Appearances = n)
df_women <- rename(df_women, Average_Placement = Rank, Appearances = n)

## Read in altitude and location dataset
alt <- read.csv("Data/Altitude_Data/XC_Team_Elevation_Lat_long.csv")

## Merge with existing dataset
df_men_alt <- df_men %>% left_join(alt, by = "Team")
df_women_alt <- df_women %>% left_join(alt, by = "Team")

df_alt <- rbind(df_men_alt, df_women_alt)

## Round number
df_alt<- df_alt %>% mutate_at(vars(Average_Placement), ~round(.,1))

## Write to csv
write.csv(df_alt, "Data/Ranking_Data/team_caliber.csv", row.names = FALSE)