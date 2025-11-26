library(dplyr)
library(BayesFactor)
library(BayesFactor)

data_dir <- "C:/Users/apc12/Desktop/CurvatureData"
output_dir <- "C:/Users/apc12/Desktop/ExperimentData"

files <- list.files(data_dir, pattern = "\\.csv$", full.names = TRUE)
files <- files[order(files)]
get_participant_number <- function(filepath) {
     fname <- basename(filepath)                 # get filename only
     part_num <- substr(fname, 1, 2)             # first two characters
     return(part_num)
}

get_participant_number <- function(filepath) {
  fname <- basename(filepath)
  part_num <- substr(fname, 1, 2)
  return(part_num)
}

master_df <- read.csv(files[1], header = TRUE)
master_df$ParticipantNumber <- get_participant_number(files[1])

for (f in files[-1]) {
     temp <- read.csv(f, header = TRUE)
     temp <- temp[-1, ]                          # drop header row
     names(temp) <- names(master_df)[names(master_df) != "ParticipantNumber"]
 
   
   temp$ParticipantNumber <- get_participant_number(f)
   master_df <- rbind(master_df, temp)
}

write.csv(master_df, "C:/Users/apc12/Desktop/ExperimentData/AllParticipants_combined.csv", 
          row.names = FALSE)
head(master_df)

data <- read.csv("C:/Users/apc12/Desktop/CurvatureData/AllParticipants_uniqueTrials.csv")

#remove duplicate trial answers - keep smallest angle entry
data_unique <- data %>%
  group_by(ParticipantNumber, ConditionID) %>%
  arrange(MeasuredAngle, desc(Time), .by_group = TRUE) %>%
  slice(1) %>%         
  ungroup()

subject_means <- data_unique %>%
  group_by(ParticipantNumber) %>%
  summarise(
    mean_Time         = mean(Time, na.rm = TRUE),
    mean_TrialNumber  = mean(TrialNumber, na.rm = TRUE),
    mean_Distance     = mean(Distance, na.rm = TRUE),
    mean_StartAngle   = mean(StartAngle, na.rm = TRUE),
    mean_MeasuredAngle = mean(MeasuredAngle, na.rm = TRUE),
    mean_HMDHeight    = mean(HMDHeight, na.rm = TRUE),
    n_conditions      = n()   #should be 60
  )

#find outliers
data_with_flags <- data_unique %>%
  group_by(ParticipantNumber) %>%
  mutate(
    angle_z = scale(MeasuredAngle),
    angle_outlier = abs(angle_z) > 3
  )

data_with_flags %>% filter(angle_outlier)

#deleted measured angle value for incident with one subject using wrong end of pointer forone trial
data %>% 
  filter(!(ParticipantNumber == 11 & ConditionID == 19))



#mean of each column per participant
subject_means <- data %>%
  group_by(ParticipantNumber) %>%
  summarise(
    across(where(is.numeric), ~ mean(.x, na.rm = TRUE))
  )
print(subject_means)


# Data analysis 

install.packages("BayesFactor")
library(BayesFactor)
library(dplyr)

data <- data %>%
  mutate(
    Error = MeasuredAngle,        # signed error
    AbsError = abs(MeasuredAngle) # absolute val
  )

within_subject_means <- data %>%
  group_by(ParticipantNumber) %>%
  summarise(
    mean_Error = mean(Error, na.rm = TRUE),
    mean_AbsError = mean(abs(Error), na.rm = TRUE),
    n_trials = n()
  )
print(within_subject_means)

bf_error <- ttestBF(
  x = subject_means$mean_Error,
  mu = 0
)
bf_error


within_subject_by_distance <- data %>%
  group_by(ParticipantNumber, Distance) %>%   # <-- subject × distance
  summarise(
    mean_Error = mean(Error, na.rm = TRUE),
    mean_AbsError = mean(AbsError, na.rm = TRUE),
    n_trials = n()
  ) %>%
  ungroup()
print(within_subject_by_distance)

within_subject_by_distance <- within_subject_by_distance %>%
  mutate(
    ParticipantNumber = factor(ParticipantNumber),
    Distance = factor(Distance)   # treat distances as categorical levels
  )



library(BayesFactor)

bf_distance <- anovaBF(
  mean_Error ~ Distance + ParticipantNumber,
  data = within_subject_by_distance,
  whichRandom = "ParticipantNumber"
)
bf_distance


library(ggplot2)

ggplot(within_subject_by_distance, aes(x = Distance, y = mean_Error, group = ParticipantNumber)) +
  geom_line(alpha = 0.4) +
  geom_point(size = 2) +
  stat_summary(fun = mean, geom = "line", linewidth = 1.2, color = "blue") +
  labs(
    title = "Within-Subject Mean Error by Distance",
    subtitle = "Red line = Group Mean"
  )

within_subject_by_distance %>%
  group_by(Distance) %>%
  summarise(group_mean = mean(mean_Error), group_sd = sd(mean_Error))

data %>%
  group_by(ParticipantNumber, Distance) %>%
  summarise(sd = sd(Error))

