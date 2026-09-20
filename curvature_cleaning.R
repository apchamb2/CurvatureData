library(dplyr)

data_dir <- "C:/Your/Path"

files <- list.files(data_dir, pattern = "\\.csv$", full.names = TRUE)
files <- files[order(files)]
get_participant_number <- function(filepath) {
     fname <- basename(filepath)                 # get filename only
     part_num <- substr(fname, 1, 2)             # first two characters
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

data <- read.csv("C:/Users/apc12/Desktop/ExperimentData/AllParticipants_combined.csv")

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












#mean of each column per participant
subject_means <- data %>%
  group_by(ParticipantNumber) %>%
  summarise(
    across(where(is.numeric), ~ mean(.x, na.rm = TRUE))
  )
print(subject_means)


