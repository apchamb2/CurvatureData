library(dplyr)

data_dir <- "C:/Users/apc12/Desktop/ExperimentData"

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
head(data)
str(data)

#mean of each column per participant
subject_means <- data %>%
  group_by(ParticipantNumber) %>%
  summarise(
    across(where(is.numeric), ~ mean(.x, na.rm = TRUE))
  )
print(subject_means)


